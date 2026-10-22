#!/usr/bin/env python3
"""Validate and package one final image post in its explicit reading order."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import sys
import zipfile

from preview_covers import PRESETS, png_size


def load_pages(manifest):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or type(data.get("schemaVersion")) is not int or data["schemaVersion"] != 1:
        raise ValueError("Unsupported delivery schemaVersion (expected 1)")
    presets = json.loads(PRESETS.read_text(encoding="utf-8"))
    placement = data.get("placement")
    if not isinstance(placement, str) or placement not in presets["placements"]:
        raise ValueError("placement must be xhs-note or douyin-note")
    scope = data.get("scope")
    if scope not in ("cover", "body", "set"):
        raise ValueError("scope must be cover, body or set")
    count = data.get("bodyPageCount")
    if type(count) is not int or count < 0 or (count == 0) != (scope == "cover"):
        raise ValueError("bodyPageCount must match the planned scope (positive for body/set)")
    pages = data.get("pages")
    if not isinstance(pages, list) or not pages:
        raise ValueError("pages must be a non-empty list of selected final images")
    prepared, orders, digests = [], set(), set()
    for page in pages:
        if not isinstance(page, dict):
            raise ValueError("Every page must be an object")
        order = page.get("order")
        if type(order) is not int or order < 1 or order in orders:
            raise ValueError("Page order must be a unique positive integer")
        orders.add(order)
        if page.get("role") not in ("cover", "body"):
            raise ValueError("Page role must be cover or body")
        if page.get("status") != "final" or page.get("reviewStatus") != "reviewed":
            raise ValueError("Only final images marked reviewed can be packaged; exclude drafts/revisions")
        if page.get("placement", placement) != placement:
            raise ValueError("Package each platform separately")
        if not isinstance(page.get("title"), str) or not page["title"].strip():
            raise ValueError("Each page needs its expected title")
        image = page.get("image")
        if not isinstance(image, str) or not image or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", image):
            raise ValueError("image must be a local PNG path")
        source = (manifest.parent / image).resolve()
        if source.suffix.lower() != ".png" or not source.is_file():
            raise ValueError(f"Missing or unsupported PNG: {image}")
        size = png_size(source)
        ratio = presets["placements"][placement]["ratio"]
        if size[0] * ratio[1] != size[1] * ratio[0]:
            raise ValueError(f"Final image must be {ratio[0]}:{ratio[1]} without cropping: {image}")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        if digest in digests:
            raise ValueError("Duplicate image content: select each final image only once")
        digests.add(digest)
        prepared.append({"order": order, "role": page["role"], "title": page["title"],
                         "status": "final", "reviewStatus": "reviewed", "sourceSize": list(size),
                         "sha256": digest, "_source": source})
    if orders != set(range(1, len(pages) + 1)):
        raise ValueError("Page order must be consecutive from 1 with no gaps")
    prepared.sort(key=lambda page: page["order"])
    covers = [page for page in prepared if page["role"] == "cover"]
    expected_covers = 0 if scope == "body" else 1
    if len(covers) != expected_covers:
        raise ValueError(f"{scope} requires exactly {expected_covers} cover(s); do not include alternatives")
    if covers and prepared[0]["role"] != "cover":
        raise ValueError("The selected cover must be page 1")
    if len(prepared) - len(covers) != count:
        raise ValueError("Final body page count does not match planned bodyPageCount")
    body_index = 0
    number_width = max(2, len(str(len(prepared))))
    for page in prepared:
        if page["role"] == "body":
            body_index += 1
            name, label = f'body-{body_index:02}', f"正文{body_index:02}"
        else:
            name, label = "cover", "封面"
        page["image"] = f'images/{page["order"]:0{number_width}}-{name}.png'
        page["label"] = f'第{page["order"]}张 · {label}'
    return data, prepared, presets["placements"][placement]["name"]


def render(topic, placement_name, pages):
    escape = html.escape
    figures = []
    for page in pages:
        caption = escape(f'{page["label"]}：{page["title"]}')
        figures.append(f'<figure><figcaption>{caption}</figcaption>'
                       f'<a href="{page["image"]}"><img src="{page["image"]}" alt="{caption}"></a></figure>')
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>最终图片顺序</title><style>
*{box-sizing:border-box}body{margin:0;background:#f6f6f3;color:#20252a;font:16px/1.6 system-ui,sans-serif}
main{max-width:600px;margin:auto;padding:24px 16px}h1{font-size:24px}figure{margin:32px 0}
figcaption{margin-bottom:10px;font-weight:600}img{display:block;width:100%;height:auto}
a{color:#2457a0}small{display:block;color:#555}
</style><main><h1>''' + escape(str(topic)) + "</h1><p>" + escape(placement_name) + f' · 共{len(pages)}张，按下方顺序使用。</p>' + \
        '<p><a href="final-images.zip">下载最终原图 ZIP</a></p><small>仅展示选定最终版。复核标记来自输入清单；打包不执行OCR或平台上传验证。</small>' + \
        "".join(figures) + "</main></html>"


def build(manifest, out_dir):
    manifest, out_dir = Path(manifest).resolve(), Path(out_dir).resolve()
    if out_dir.exists():
        raise ValueError(f"Output already exists; choose a new directory: {out_dir}")
    data, pages, placement_name = load_pages(manifest)
    # All input and ordering checks happen before creating a delivery directory.
    (out_dir / "images").mkdir(parents=True)
    with zipfile.ZipFile(out_dir / "final-images.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for page in pages:
            content = page.pop("_source").read_bytes()
            if hashlib.sha256(content).hexdigest() != page["sha256"]:
                raise ValueError("Source changed while packaging; choose a new output directory and retry")
            (out_dir / page["image"]).write_bytes(content)
            archive.writestr(Path(page["image"]).name, content)
    report = {"schemaVersion": 1, "topic": data.get("topic", "最终图片"),
              "placement": data["placement"], "scope": data["scope"],
              "bodyPageCount": data["bodyPageCount"], "pages": pages}
    (out_dir / "delivery.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "index.html").write_text(render(report["topic"], placement_name, pages), encoding="utf-8")
    lines = [f'# {report["topic"]}', "", f"{placement_name}，共{len(pages)}张，按以下顺序使用。", ""]
    for page in pages:
        lines.append(f'{page["order"]}. [{page["label"]}：{page["title"]}]({page["image"]})')
    lines.extend(["", "[下载最终原图 ZIP](final-images.zip)", "",
                  "复核标记来自输入清单；此脚本只校验交付结构，不执行OCR或平台上传验证。", ""])
    (out_dir / "delivery.md").write_text("\n".join(lines), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = build(args.manifest, args.out_dir)
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    print(f'Final delivery: {args.out_dir / "index.html"}')
    for page in report["pages"]:
        print(f'{page["label"]}：{page["title"]} -> {args.out_dir / page["image"]}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
