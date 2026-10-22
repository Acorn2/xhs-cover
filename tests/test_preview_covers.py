import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("preview", ROOT / "atutun-xhs-cover/scripts/preview_covers.py")
preview = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preview)
PRESETS = json.loads(preview.PRESETS.read_text())
IMAGE = ROOT / "examples/03-beginner-qa.png"


class GeometryTests(unittest.TestCase):
    def test_portrait_to_wide_crops_height(self):
        crop = preview.crop_box(3 / 4, 2.35)
        self.assertAlmostEqual(crop[2], 1)
        self.assertAlmostEqual(crop[3], (3 / 4) / 2.35)
        self.assertFalse(preview.contains(crop, [0.07, 0.06, 0.86, 0.32]))

    def test_align_top_preserves_top(self):
        crop = preview.crop_box(3 / 4, 1, (0.5, 0))
        self.assertEqual(crop[1], 0)
        self.assertTrue(preview.contains(crop, [0.07, 0.06, 0.86, 0.32]))

    def test_user_supplied_overlay_and_safe_area(self):
        item = {"id": "note", "placement": "douyin-note", "style": "01",
                "title": "测试", "sourceSize": [1080, 1440], "position": [0.5, 0.5],
                "importantRegions": [{"label": "标题", "box": [0.87, 0.4, 0.1, 0.2]}]}
        preset = copy.deepcopy(PRESETS["placements"]["douyin-note"])
        preset["overlays"] = [{"name": "人工提供的占位", "box": [0.9, 0.3, 0.1, 0.5]}]
        result = preview.inspect(item, preset)
        self.assertTrue(any("重叠" in x for x in result["warnings"]))
        self.assertTrue(any("安全框" in x for x in result["warnings"]))

    def test_missing_annotations_is_not_pass(self):
        item = {"id": "xhs", "placement": "xhs-note", "style": "03", "title": "测试",
                "sourceSize": [1080, 1440], "position": [0.5, 0.5], "importantRegions": []}
        result = preview.inspect(item, PRESETS["placements"]["xhs-note"])
        self.assertEqual(result["status"], "needs_review")
        self.assertTrue(any("没有重要区域" in x for x in result["warnings"]))

    def test_invalid_rectangle_and_nonfinite(self):
        for box in [[0, 0, 0, 1], [0.8, 0, 0.3, 0.1], [0, 0, float("nan"), 1], [True, 0, 0.5, 1]]:
            with self.subTest(box=box), self.assertRaises(ValueError):
                preview.rectangle(box, "test")


class BuildTests(unittest.TestCase):
    def setUp(self):
        (ROOT / ".tmp").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="preview-tests-", dir=ROOT / ".tmp")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / "input.json"
        self.data = {"schemaVersion": 1, "topic": "<script>alert(1)</script>",
                     "variants": [{"id": "sample", "placement": "douyin-note", "style": "09",
                                   "title": "AI智能体", "image": str(IMAGE),
                                   "importantRegions": [{"label": "标题", "box": [0.92, 0.1, 0.05, 0.1]}]}]}

    def write(self, data=None):
        self.manifest.write_text(json.dumps(data or self.data), encoding="utf-8")

    def test_build_preserves_source_and_warns_about_margin(self):
        self.write()
        original = IMAGE.read_bytes()
        report = preview.build(self.manifest, self.root / "out")
        self.assertEqual(IMAGE.read_bytes(), original)
        self.assertEqual((self.root / "out/assets/sample.png").read_bytes(), original)
        self.assertTrue(report["variants"][0]["needs_relayout"])
        self.assertTrue(any("标题超出建议安全框" in x for x in report["variants"][0]["warnings"]))
        document = (self.root / "out/index.html").read_text()
        self.assertNotIn("<script>alert", document)
        self.assertIn("&lt;script&gt;", document)
        self.assertEqual(json.loads((self.root / "out/report.json").read_text()), report)
        with self.assertRaises(ValueError):
            preview.build(self.manifest, self.root / "out")

    def test_rejects_bad_input_before_creating_output(self):
        changes = [{"placement": "wechat-channels"}, {"placement": "douyin-video"},
                   {"placement": "wechat-head"}, {"placement": "wechat-square"}, {"image": "missing.png"},
                   {"id": "../escape"}, {"position": [1.1, 0.5]},
                   {"style": "13"}, {"image": "https://example.com/image.png"},
                   {"image": str(IMAGE.with_suffix(".jpg"))},
                   {"importantRegions": [{"label": "标题", "box": [0, 0, 2, 1]}]}]
        for i, change in enumerate(changes):
            with self.subTest(change=change):
                data = copy.deepcopy(self.data)
                data["variants"][0].update(change)
                self.write(data)
                out = self.root / f"bad-{i}"
                with self.assertRaises(ValueError):
                    preview.build(self.manifest, out)
                self.assertFalse(out.exists())

    def test_duplicate_ids(self):
        self.data["variants"].append(copy.deepcopy(self.data["variants"][0]))
        self.write()
        with self.assertRaises(ValueError):
            preview.build(self.manifest, self.root / "out")

    def test_both_image_post_platforms_keep_full_three_by_four(self):
        for placement in ("xhs-note", "douyin-note"):
            with self.subTest(placement=placement):
                data = copy.deepcopy(self.data)
                data["variants"][0]["placement"] = placement
                data["variants"][0]["importantRegions"] = [{"label": "主体", "box": [0.2, 0.2, 0.6, 0.6]}]
                self.write(data)
                report = preview.build(self.manifest, self.root / placement)
                result = report["variants"][0]
                self.assertFalse(result["needs_relayout"])
                self.assertEqual(result["previews"][0]["crop"], [0, 0, 1, 1])

    def test_png_validation(self):
        self.assertEqual(preview.png_size(IMAGE), (1086, 1448))
        broken = self.root / "broken.png"
        broken.write_bytes(b"not a png")
        with self.assertRaises(ValueError):
            preview.png_size(broken)


if __name__ == "__main__":
    unittest.main()
