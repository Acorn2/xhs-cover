#!/usr/bin/env python3
"""Check generated cover and body images offline without changing their source PNGs."""
import argparse
import html
import json
import math
from pathlib import Path
import re
import shutil
import struct
import sys

PRESETS = Path(__file__).resolve().parents[1] / "references/platform-presets.json"
BODY_THEMES = ("body-clean", "body-sketch", "body-editorial", "body-duotone-print",
               "body-crayon", "body-digital-notes", "body-paper-collage", "body-chalkboard")


def numbers(value, length, name):
    if not isinstance(value, list) or len(value) != length:
        raise ValueError(f"{name} must have {length} numbers")
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in value):
        raise ValueError(f"{name} must contain finite numbers")
    return value


def rectangle(value, name):
    x, y, w, h = numbers(value, 4, name)
    if min(x, y) < 0 or min(w, h) <= 0 or x + w > 1.000000001 or y + h > 1.000000001:
        raise ValueError(f"{name} must be a positive rectangle inside [0,1]")
    return [x, y, w, h]


def png_size(path):
    with path.open("rb") as stream:
        header = stream.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"Invalid PNG header: {path.name}")
    width, height = struct.unpack(">II", header[16:24])
    if not width or not height:
        raise ValueError(f"Invalid image dimensions: {path.name}")
    return width, height


def crop_box(source_ratio, target_ratio, position=(0.5, 0.5)):
    width = min(1.0, target_ratio / source_ratio)
    height = min(1.0, source_ratio / target_ratio)
    return [(1 - width) * position[0], (1 - height) * position[1], width, height]


def contains(outer, inner):
    x, y, w, h = outer
    a, b, c, d = inner
    return a >= x - 1e-9 and b >= y - 1e-9 and a + c <= x + w + 1e-9 and b + d <= y + h + 1e-9


def overlaps(a, b):
    return max(a[0], b[0]) < min(a[0] + a[2], b[0] + b[2]) and max(a[1], b[1]) < min(a[1] + a[3], b[1] + b[3])


def project(box, crop):
    return [(box[0] - crop[0]) / crop[2], (box[1] - crop[1]) / crop[3],
            box[2] / crop[2], box[3] / crop[3]]


def load_request(manifest, presets):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schemaVersion") != 1:
        raise ValueError("Unsupported manifest schemaVersion (expected 1)")
    variants = data.get("variants")
    if not isinstance(variants, list) or not variants:
        raise ValueError("variants must be a non-empty list")
    seen, prepared = set(), []
    for item in variants:
        if not isinstance(item, dict):
            raise ValueError("Every variant must be an object")
        ident = item.get("id", "")
        if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,63}", ident) or ident in seen:
            raise ValueError("Variant id must be unique and use lowercase letters, digits, _ or -")
        seen.add(ident)
        placement = item.get("placement")
        if not isinstance(placement, str) or placement not in presets["placements"]:
            raise ValueError(f"Unknown placement: {placement}")
        if item.get("style") not in [f"{x:02}" for x in range(1, 13)] + list(BODY_THEMES):
            raise ValueError("style must be 01 to 12 or one of: " + ", ".join(BODY_THEMES))
        if not isinstance(item.get("title"), str) or not item["title"].strip():
            raise ValueError("Each variant needs its expected title")
        image = item.get("image")
        if not isinstance(image, str) or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", image):
            raise ValueError("image must be a local PNG path")
        source = (manifest.parent / image).resolve()
        if source.suffix.lower() != ".png" or not source.is_file():
            raise ValueError(f"Missing or unsupported PNG: {image}")
        size = png_size(source)
        position = numbers(item.get("position", [0.5, 0.5]), 2, "position")
        if any(x < 0 or x > 1 for x in position):
            raise ValueError("position must be inside [0,1]")
        regions = item.get("importantRegions", [])
        if not isinstance(regions, list):
            raise ValueError("importantRegions must be a list")
        for region in regions:
            if not isinstance(region, dict) or not isinstance(region.get("label"), str) or not region["label"].strip():
                raise ValueError("Each important region needs a label")
            rectangle(region.get("box"), "importantRegions.box")
        prepared.append({**item, "position": position, "importantRegions": regions,
                         "_source": source, "sourceSize": list(size)})
    return data, prepared


def inspect(item, preset):
    source_ratio = item["sourceSize"][0] / item["sourceSize"][1]
    target_ratio = preset["ratio"][0] / preset["ratio"][1]
    warnings = []
    if abs(source_ratio / target_ratio - 1) > 0.015:
        warnings.append("原图与目标比例不同，当前仅做裁切检查，需要重新布局")
    if not item["importantRegions"]:
        warnings.append("没有重要区域标注，尚未检查标题、正文或主体")
    views = []
    for index, view in enumerate(preset["previews"]):
        ratio = view["ratio"][0] / view["ratio"][1]
        crop = crop_box(source_ratio, ratio, item["position"])
        issues = []
        for region in item["importantRegions"]:
            if not contains(crop, region["box"]):
                issues.append(f'{region["label"]}被裁切')
            if index == 0:
                mapped = project(region["box"], crop)
                if not contains(preset["safe"], mapped):
                    issues.append(f'{region["label"]}超出建议安全框')
                for overlay in preset["overlays"]:
                    if overlaps(mapped, overlay["box"]):
                        issues.append(f'{region["label"]}与{overlay["name"]}重叠')
        views.append({**view, "crop": crop, "issues": issues})
        warnings.extend(f'{view["name"]}：{issue}' for issue in issues)
    return {"id": item["id"], "placement": item["placement"], "style": item["style"],
            "title": item["title"], "sourceSize": item["sourceSize"], "targetSize": preset["size"],
            "status": "needs_review", "needs_relayout": bool(warnings),
            "warnings": warnings, "previews": views}


def box_css(box):
    return ";".join(f"{key}:{value * 100:.6f}%" for key, value in zip(("left", "top", "width", "height"), box))


def render(items, reports, presets, topic):
    escape = html.escape
    sections = []
    for item, report in zip(items, reports):
        preset = presets["placements"][item["placement"]]
        asset = f'assets/{item["id"]}.png'
        position = f'{item["position"][0] * 100}% {item["position"][1] * 100}%'
        views = []
        for index, view in enumerate(report["previews"]):
            masks = ""
            if index == 0:
                masks += f'<span class="safe" style="{box_css(preset["safe"])}"></span>'
                for overlay in preset["overlays"]:
                    masks += f'<span class="mask" style="{box_css(overlay["box"])}">{escape(overlay["name"])}</span>'
            ratio = f'{view["ratio"][0]}/{view["ratio"][1]}'
            image = f'<img src="{asset}" alt="{escape(item["title"], quote=True)}" style="object-position:{position}">'
            views.append(f'<figure><figcaption>{escape(view["name"])}</figcaption><div class="frame" style="aspect-ratio:{ratio}">{image}{masks}</div><div class="thumb" style="aspect-ratio:{ratio}">{image}</div></figure>')
        warnings = "".join(f"<li>{escape(w)}</li>" for w in report["warnings"])
        note = warnings or "<li>结构检查未发现上述风险，仍需目视复核</li>"
        sections.append(f'<section><h2>{escape(preset["name"])} · 风格{item["style"]}</h2><p>{escape(item["title"])} · 原图{item["sourceSize"][0]}×{item["sourceSize"][1]} · 待目视复核</p><div class="views"><figure><figcaption>原图（完整显示）</figcaption><img class="original" src="{asset}" alt="原图"></figure>{"".join(views)}</div><ul>{note}</ul></section>')
    return """<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>封面与正文图展示检查</title><style>
*{box-sizing:border-box}body{margin:0;background:#f3f4f6;color:#18202b;font:15px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif}main{max-width:1440px;padding:28px;margin:auto}h1{font-size:28px}h2{font-size:22px}section{background:white;border:1px solid #d4d8df;margin:24px 0;padding:20px;border-radius:8px}.views{display:flex;flex-wrap:wrap;gap:24px;align-items:start}figure{margin:0;width:260px;max-width:100%}figcaption{margin-bottom:8px;font-weight:600}.original{display:block;width:100%;height:260px;object-fit:contain;background:#eef0f3}.frame,.thumb{position:relative;overflow:hidden;background:#dce0e5}.frame{width:100%}.thumb{width:104px;margin-top:12px}.frame img,.thumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.safe,.mask{position:absolute;pointer-events:none}.safe{border:2px dashed #21b868}.mask{background:#d8474755;font-size:10px;color:#841f28;overflow:hidden}li{margin:4px 0}header p{max-width:80ch}footer{color:#626c7a}@media(max-width:600px){main{padding:14px}section{padding:14px}.views{gap:18px}figure{width:100%;max-width:320px}}
</style><main><header><h1>""" + escape(str(topic)) + """ · 封面与正文图展示检查</h1><p>这是生图后的检查工具，不负责平台策略或独立生图。绿框为建议基础边距，小图检查层级；正文可读性还需查看原图与手机阅读尺寸。默认3:4整图，不做跨平台裁切。原图未修改，未执行OCR，所有结果均待目视复核。</p></header>""" + "".join(sections) + "<footer>预设更新：" + escape(presets["updated"]) + "</footer></main></html>"


def build(manifest, out_dir):
    manifest, out_dir = Path(manifest).resolve(), Path(out_dir).resolve()
    if out_dir.exists():
        raise ValueError(f"Output already exists; choose a new directory: {out_dir}")
    presets = json.loads(PRESETS.read_text(encoding="utf-8"))
    data, items = load_request(manifest, presets)
    reports = [inspect(item, presets["placements"][item["placement"]]) for item in items]
    document = render(items, reports, presets, data.get("topic", "封面"))
    # Validate every input before creating any output.
    (out_dir / "assets").mkdir(parents=True)
    for item in items:
        shutil.copyfile(item["_source"], out_dir / "assets" / f'{item["id"]}.png')
    report = {"schemaVersion": 1, "status": "needs_review", "presetUpdated": presets["updated"],
              "notice": presets["notice"], "variants": reports}
    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "index.html").write_text(document, encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = build(args.manifest, args.out_dir)
    except (ValueError, OSError, KeyError, TypeError, struct.error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    print(f"Preview: {args.out_dir / 'index.html'}")
    print(f"{len(report['variants'])} variants; all need visual review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
