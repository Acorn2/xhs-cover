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
                     "scope": "set", "bodyPageCount": 2, "pages": []}
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
        report = package.build(self.manifest, out)
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
        self.assertEqual(json.loads((out / "delivery.json").read_text()), report)
        self.assertIn("第2张 · 正文01", (out / "delivery.md").read_text())

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
        self.assertTrue((out / "final-images.zip").is_file())


if __name__ == "__main__":
    unittest.main()
