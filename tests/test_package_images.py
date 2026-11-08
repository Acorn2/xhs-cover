import copy
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "atutun-xhs-cover/scripts/package_images.py"
SPEC = importlib.util.spec_from_file_location("package_images", SCRIPT)
package = importlib.util.module_from_spec(SPEC)
with patch.object(sys, "path", [str(SCRIPT.parent), *sys.path]):
    SPEC.loader.exec_module(package)


def png_bytes(red, width=3, height=4):
    def chunk(kind, content):
        return struct.pack(">I", len(content)) + kind + content + struct.pack(">I", zlib.crc32(kind + content))
    rows = (b"\x00" + bytes([red, 30, 60]) * width) * height
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


class PackageTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".tmp").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="package-tests-", dir=ROOT / ".tmp")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / "selected.json"
        self.data = {"schemaVersion": 1, "topic": "<script>测试</script>", "placement": "xhs-note",
                     "scope": "set", "bodyPageCount": 2, "pages": [],
                     "publication": {"title": "给文章配图，我给AI立了条规矩",
                                     "alternatives": ["文章配图，别再拿灯泡糊弄我了"],
                                     "tags": ["文章配图", "#AI工具", "Codex"]}}
        for order, (role, name) in enumerate((("cover", "cover-v2"), ("body", "explain"), ("body", "try")), 1):
            (self.root / f"{name}.png").write_bytes(png_bytes(order))
            self.data["pages"].append({"order": order, "role": role, "title": f"页面{order}",
                                       "image": f"{name}.png", "status": "final", "reviewStatus": "reviewed"})
        # An unselected revision must never enter a package by directory scanning.
        (self.root / "cover-v1.png").write_bytes(png_bytes(99))

    def write(self, data=None):
        self.manifest.write_text(json.dumps(self.data if data is None else data), encoding="utf-8")

    def reject(self, data):
        self.write(data)
        out = self.root / "rejected"
        with self.assertRaises(ValueError):
            package.build(self.manifest, out)
        self.assertFalse(out.exists())

    def test_unordered_input_exports_one_cover_and_ordered_body_without_history(self):
        self.data["pages"].reverse()
        self.write()
        originals = {p.name: p.read_bytes() for p in self.root.glob("*.png")}
        out = self.root / "final"
        report = package.build(self.manifest, out, create_zip=True)
        names = ["01-cover.png", "02-body-01.png", "03-body-02.png"]
        self.assertEqual([p["order"] for p in report["pages"]], [1, 2, 3])
        self.assertEqual(sorted(p.name for p in (out / "images").iterdir()), names)
        with zipfile.ZipFile(out / "final-images.zip") as archive:
            self.assertEqual(archive.namelist(), names)
            for name, source in zip(names, ("cover-v2.png", "explain.png", "try.png")):
                self.assertEqual(archive.read(name), originals[source])
                self.assertEqual((out / "images" / name).read_bytes(), originals[source])
        self.assertEqual(originals, {p.name: p.read_bytes() for p in self.root.glob("*.png")})
        document = (out / "index.html").read_text()
        self.assertEqual(document.count("<figure>"), 3)
        self.assertEqual(document.count("<img "), 3)
        self.assertLess(document.index("页面1"), document.index("页面2"))
        self.assertLess(document.index("页面2"), document.index("页面3"))
        self.assertNotIn("cover-v1", document)
        self.assertNotIn("<script>", document)
        self.assertIn("&lt;script&gt;", document)
        self.assertIn("第2张 · 正文01", document)
        self.assertEqual({p.name for p in out.iterdir()},
                         {"images", "index.html", "publication.md", "final-images.zip"})

    def test_two_covers_are_rejected_before_output(self):
        self.data["pages"][1]["role"] = "cover"
        self.reject(self.data)

    def test_cover_must_be_first(self):
        self.data["pages"][0]["order"], self.data["pages"][1]["order"] = 2, 1
        self.reject(self.data)

    def test_duplicate_missing_and_invalid_orders_are_rejected(self):
        for order in (1, 4, 0, -1, True, "2", 2.0, None):
            with self.subTest(order=order):
                data = copy.deepcopy(self.data)
                data["pages"][1]["order"] = order
                self.reject(data)

    def test_incomplete_planned_series_is_rejected(self):
        self.data["pages"].pop()
        self.reject(self.data)

    def test_only_selected_final_reviewed_pages_are_allowed(self):
        for changes in ({"status": "draft"}, {"status": "superseded"}, {"status": None},
                        {"reviewStatus": "needs_review"}, {"reviewStatus": None}):
            with self.subTest(changes=changes):
                data = copy.deepcopy(self.data)
                data["pages"][0].update(changes)
                self.reject(data)

    def test_version_two_hresh_cover_requires_typography_review_record(self):
        self.data["schemaVersion"] = 2
        cover = self.data["pages"][0]
        self.reject(self.data)
        cover["typographyStandard"] = "hresh-confirmed"
        self.reject(self.data)
        review = {key: True for key in ("referenceCompared", "glyphsCompared", "effectsCompared",
                                        "textCompared", "thumbnailCompared")}
        review["comparisonRecord"] = "work.md"
        cover["typographyReview"] = review
        self.reject(self.data)
        (self.root / "work.md").write_text("   ")
        self.reject(self.data)
        (self.root / "work.md").write_text("Manually compared the cover with the reference.")
        for key in ("referenceCompared", "glyphsCompared", "effectsCompared", "textCompared", "thumbnailCompared"):
            with self.subTest(missing=key):
                broken = copy.deepcopy(self.data)
                broken["pages"][0]["typographyReview"][key] = False
                self.reject(broken)
        self.write()
        self.assertEqual(len(package.build(self.manifest, self.root / "reviewed")["pages"]), 3)

    def test_version_two_other_cover_requires_explicit_explanation(self):
        self.data["schemaVersion"] = 2
        cover = self.data["pages"][0]
        cover["typographyStandard"] = "other"
        self.reject(self.data)
        cover["typographyException"] = "Non-Hresh cover"
        self.write()
        self.assertEqual(len(package.build(self.manifest, self.root / "other")["pages"]), 3)

    def test_duplicate_image_content_is_rejected_even_under_a_different_filename(self):
        (self.root / "renamed.png").write_bytes((self.root / "explain.png").read_bytes())
        self.data["pages"][2]["image"] = "renamed.png"
        self.reject(self.data)

    def test_invalid_inputs_do_not_create_output(self):
        for changes in ({"role": "revision"}, {"title": " "}, {"image": "missing.png"},
                        {"image": "https://example.com/test.png"}, {"image": "file:///tmp/test.png"},
                        {"placement": "douyin-note"}):
            with self.subTest(changes=changes):
                data = copy.deepcopy(self.data)
                data["pages"][1].update(changes)
                self.reject(data)
        for changes in ({"placement": "douyin-video"}, {"scope": "comparison"},
                        {"bodyPageCount": 3}, {"bodyPageCount": True}, {"pages": []}):
            with self.subTest(changes=changes):
                self.reject({**self.data, **changes})

    def test_wrong_ratio_and_broken_png_are_rejected(self):
        for content in (png_bytes(20, 4, 3), b"not PNG"):
            with self.subTest(content=content):
                (self.root / "try.png").write_bytes(content)
                self.reject(self.data)

    def test_cover_only_and_body_only_work_for_each_platform(self):
        for placement in ("xhs-note", "douyin-note"):
            for scope in ("cover", "body"):
                with self.subTest(placement=placement, scope=scope):
                    data = copy.deepcopy(self.data)
                    data.update(placement=placement, scope=scope, bodyPageCount=0 if scope == "cover" else 2)
                    data["pages"] = [p for p in data["pages"] if p["role"] == scope]
                    for order, page in enumerate(data["pages"], 1):
                        page["order"] = order
                    self.write(data)
                    result = package.build(self.manifest, self.root / f"{placement}-{scope}")
                    self.assertEqual(len(result["pages"]), 1 if scope == "cover" else 2)
                    self.assertEqual(result["pages"][0]["label"], "第1张 · 封面" if scope == "cover" else "第1张 · 正文01")

    def test_existing_output_is_never_overwritten(self):
        self.write()
        out = self.root / "existing"
        out.mkdir()
        marker = out / "user-file.txt"
        marker.write_text("keep")
        with self.assertRaises(ValueError):
            package.build(self.manifest, out)
        self.assertEqual(list(out.iterdir()), [marker])
        self.assertEqual(marker.read_text(), "keep")

    def test_cli_failure_and_success(self):
        self.data["pages"][1]["role"] = "cover"
        self.write()
        out = self.root / "cli"
        result = subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(self.manifest),
                                 "--out-dir", str(out)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("exactly 1 cover", result.stderr)
        self.assertFalse(out.exists())
        self.data["pages"][1]["role"] = "body"
        self.write()
        result = subprocess.run([sys.executable, str(SCRIPT), "--manifest", str(self.manifest),
                                 "--out-dir", str(out)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("第1张 · 封面", result.stdout)
        self.assertFalse((out / "final-images.zip").exists())

    def test_default_delivery_contains_only_images_preview_and_copy(self):
        body = "先圈出读者最容易卡住的地方，再决定画什么。"
        self.data["publication"]["body"] = body
        self.write()
        out = self.root / "with-publication"
        result = package.build(self.manifest, out)
        publication = result["publication"]
        self.assertEqual(publication["title"], self.data["publication"]["title"])
        self.assertEqual(publication["titleChars"], 15)
        self.assertEqual(publication["alternativeTitleChars"], [14])
        self.assertEqual(publication["tags"], ["文章配图", "AI工具", "Codex"])
        self.assertEqual(publication["body"], body)
        for filename in ("index.html", "publication.md"):
            document = (out / filename).read_text()
            self.assertIn(publication["title"], document)
            self.assertIn(body, document)
            self.assertIn("#文章配图 #AI工具 #Codex", document)
            self.assertIn(publication["alternatives"][0], document)
        self.assertEqual((out / "index.html").read_text().count("<img "), 3)
        self.assertNotIn("final-images.zip", (out / "index.html").read_text())
        self.assertEqual({p.name for p in out.iterdir()}, {"images", "index.html", "publication.md"})
        self.assertEqual(len([p for p in out.rglob("*") if p.is_file()]), 5)

    def test_publication_update_reuses_images_and_existing_zip(self):
        self.write()
        out = self.root / "final"
        initial = package.build(self.manifest, out, create_zip=True)
        self.assertNotIn("body", initial["publication"])
        (out / "process").mkdir()
        (out / "process/work.md").write_text("Requested reproducibility notes")
        preserved = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in out.rglob("*")
                     if p.is_file() and (p.suffix in (".png", ".zip") or p.parent.name == "process")}
        body = "先确定哪一步难懂，再画清这一步的输入和结果。"
        self.data["publication"]["body"] = body
        self.write()
        updated = package.build(self.manifest, out, update_publication=True)
        self.assertEqual(updated["publication"], {**initial["publication"], "body": body})
        self.assertEqual(preserved, {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in preserved})
        for filename in ("index.html", "publication.md"):
            self.assertIn(body, (out / filename).read_text())
        self.assertIn('href="final-images.zip"', (out / "index.html").read_text())

    def test_publication_update_rejects_changed_images_or_unknown_directory_without_writes(self):
        self.write()
        for case in ("changed", "extra-image", "unknown-file", "missing-index"):
            with self.subTest(case=case):
                out = self.root / case
                package.build(self.manifest, out)
                if case == "changed":
                    (out / "images/01-cover.png").write_bytes(png_bytes(99))
                elif case == "extra-image":
                    (out / "images/extra.png").write_bytes(png_bytes(99))
                elif case == "unknown-file":
                    (out / "user.txt").write_text("keep")
                else:
                    (out / "index.html").rename(out / "removed-index.html")
                before = {p: p.read_bytes() for p in out.rglob("*") if p.is_file()}
                with self.assertRaises(ValueError):
                    package.build(self.manifest, out, update_publication=True)
                self.assertEqual(before, {p: p.read_bytes() for p in out.rglob("*") if p.is_file()})

    def test_publication_update_adds_copy_to_images_only_delivery(self):
        self.write()
        out = self.root / "final"
        package.build(self.manifest, out, images_only=True)
        self.assertFalse((out / "publication.md").exists())
        package.build(self.manifest, out, update_publication=True)
        self.assertTrue((out / "publication.md").is_file())
        self.assertFalse((out / "final-images.zip").exists())

    def test_cli_zip_and_publication_update(self):
        self.write()
        out = self.root / "cli-update"
        command = [sys.executable, str(SCRIPT), "--manifest", str(self.manifest), "--out-dir", str(out)]
        created = subprocess.run([*command, "--zip"], capture_output=True, text=True)
        self.assertEqual(created.returncode, 0, created.stderr)
        self.assertTrue((out / "final-images.zip").is_file())
        self.data["publication"]["title"] = "文章配图先想清楚"
        self.write()
        updated = subprocess.run([*command, "--update-publication"], capture_output=True, text=True)
        self.assertEqual(updated.returncode, 0, updated.stderr)
        self.assertIn("文章配图先想清楚", (out / "publication.md").read_text())

    def test_complete_set_requires_publication_before_output(self):
        self.data.pop("publication")
        self.reject(self.data)

    def test_images_only_explicitly_supports_legacy_manifests(self):
        self.data.pop("publication")
        self.write()
        out = self.root / "images-only"
        result = package.build(self.manifest, out, images_only=True)
        self.assertNotIn("publication", result)
        self.assertFalse((out / "publication.md").exists())
        self.assertEqual({p.name for p in out.iterdir()}, {"images", "index.html"})

    def test_invalid_publication_is_rejected_before_output(self):
        changes = [{"title": " "}, {"title": "a" * 21}, {"title": "标题\n另一个标题"},
                   {"body": " \n "}, {"body": ["正文"]}, {"body": None},
                   {"titleLocked": "yes"}, {"alternatives": "备选"}, {"alternatives": [" "]},
                   {"alternatives": ["a" * 21]},
                   {"alternatives": [self.data["publication"]["title"]]},
                   {"tags": []}, {"tags": "#文章配图"}, {"tags": ["AI工具", "#AI工具"]},
                   {"tags": ["#"]}, {"tags": ["AI 工具"]}, {"tags": [1]}]
        for change in changes:
            with self.subTest(change=change):
                data = copy.deepcopy(self.data)
                data["publication"].update(change)
                self.reject(data)
        for publication in (None, [], "title"):
            with self.subTest(publication=publication):
                data = copy.deepcopy(self.data)
                data["publication"] = publication
                self.reject(data)

    def test_locked_title_is_preserved_with_a_length_warning(self):
        self.data["publication"].update(title="a" * 21, titleLocked=True, alternatives=[])
        self.write()
        result = package.build(self.manifest, self.root / "locked")
        self.assertEqual(result["publication"]["title"], "a" * 21)
        self.assertEqual(result["publication"]["titleChars"], 21)
        self.assertTrue(result["publication"]["warnings"])

    def test_douyin_title_has_no_unverified_upload_limit(self):
        self.data["placement"] = "douyin-note"
        self.data["publication"]["title"] = "a" * 25
        self.write()
        result = package.build(self.manifest, self.root / "douyin-publication")
        self.assertEqual(result["publication"]["titleChars"], 25)

    def test_publication_html_is_escaped(self):
        self.data["publication"].update(title="<b>AI配图</b>", body="<em>段落</em>\n\n关键做法",
                                        alternatives=[], tags=["<svg>"])
        self.write()
        out = self.root / "escaped-publication"
        package.build(self.manifest, out)
        document = (out / "index.html").read_text()
        self.assertIn("&lt;b&gt;AI配图&lt;/b&gt;", document)
        self.assertIn("&lt;em&gt;段落&lt;/em&gt;\n\n关键做法", document)
        self.assertIn("    <em>段落</em>\n\n    关键做法", (out / "publication.md").read_text())
        self.assertIn("#&lt;svg&gt;", document)
        self.assertNotIn("<b>AI配图", document)

    def test_cli_requires_publication_unless_images_only(self):
        self.data.pop("publication")
        self.write()
        command = [sys.executable, str(SCRIPT), "--manifest", str(self.manifest),
                   "--out-dir", str(self.root / "cli-images-only")]
        rejected = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(rejected.returncode, 2)
        self.assertIn("publication", rejected.stderr)
        self.assertFalse((self.root / "cli-images-only").exists())
        accepted = subprocess.run([*command, "--images-only"], capture_output=True, text=True)
        self.assertEqual(accepted.returncode, 0, accepted.stderr)


if __name__ == "__main__":
    unittest.main()
