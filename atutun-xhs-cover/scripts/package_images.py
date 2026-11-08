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


def load_publication(data):
    if "publication" not in data:
        if data["scope"] == "set":
            raise ValueError("Complete sets need publication title/tags; use --images-only when explicitly requested")
        return None
    publication = data["publication"]
    if not isinstance(publication, dict):
        raise ValueError("publication must be an object")
    body = publication.get("body", "")
    if "body" in publication and (not isinstance(body, str) or not body.strip()):
        raise ValueError("publication.body must be a non-empty string when provided")
    locked = publication.get("titleLocked", False)
    if type(locked) is not bool:
        raise ValueError("publication.titleLocked must be a boolean")

    def title_text(value, allow_long=False):
        if not isinstance(value, str) or not value.strip() or len(value.splitlines()) != 1 or "\t" in value:
            raise ValueError("Publication titles must be non-empty single-line strings")
        # Editorial budget for this Skill, not a claim about the platform's API limit.
        if data["placement"] == "xhs-note" and len(value) > 20 and not allow_long:
            raise ValueError("Xiaohongshu title exceeds the 20-character editorial budget")
        return value

    title = title_text(publication.get("title"), allow_long=locked)
    alternatives = publication.get("alternatives", [])
    if not isinstance(alternatives, list):
        raise ValueError("publication.alternatives must be a list")
    alternatives = [title_text(value) for value in alternatives]
    titles = [value.strip().casefold() for value in [title, *alternatives]]
    if len(set(titles)) != len(titles):
        raise ValueError("Publication title candidates must be distinct")
    raw_tags = publication.get("tags")
    if not isinstance(raw_tags, list) or not raw_tags:
        raise ValueError("publication.tags must be a non-empty list")
    tags, seen = [], set()
    for tag in raw_tags:
        if not isinstance(tag, str):
            raise ValueError("Publication tags must be strings")
        tag = tag.strip().removeprefix("#")
        if not tag or re.search(r"[\s#]", tag) or tag.casefold() in seen:
            raise ValueError("Publication tags must be non-empty, unique and contain no spaces or embedded #")
        seen.add(tag.casefold())
        tags.append(tag)
    warnings = []
    if data["placement"] == "xhs-note" and len(title) > 20:
        warnings.append("用户锁定标题超过20字符编辑预设，已保留原文；实际发布入口限制尚未核验。")
    result = {"title": title, "titleChars": len(title), "titleLocked": locked,
              "alternatives": alternatives, "alternativeTitleChars": [len(value) for value in alternatives],
              "tags": tags, "warnings": warnings}
    if body:
        result["body"] = body.strip()
    return result


def publication_markdown(publication):
    lines = ["## 发布文案（草稿）", "", f'推荐标题（{publication["titleChars"]}字符）：',
             "", f'    {publication["title"]}', ""]
    if "body" in publication:
        lines.extend(["发布正文", ""])
        lines.extend(f"    {line}" if line else "" for line in publication["body"].splitlines())
        lines.append("")
    if publication["alternatives"]:
        lines.extend(["备选标题：", ""])
        lines.extend(f'    {title}（{len(title)}字符）' for title in publication["alternatives"])
        lines.append("")
    lines.extend(["标签：", "", "    " + " ".join(f"#{tag}" for tag in publication["tags"]), ""])
    lines.extend(publication["warnings"])
    return "\n".join(lines) + "\n"


def load_pages(manifest):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or type(data.get("schemaVersion")) is not int or data["schemaVersion"] not in (1, 2):
        raise ValueError("Unsupported delivery schemaVersion (expected 1 or 2)")
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
        if data["schemaVersion"] == 2 and page["role"] == "cover":
            standard = page.get("typographyStandard")
            if standard not in ("hresh-confirmed", "other"):
                raise ValueError("Version 2 covers need an explicit typographyStandard")
            if standard == "other":
                reason = page.get("typographyException")
                if not isinstance(reason, str) or not reason.strip():
                    raise ValueError("Other typography requires a non-empty exception or non-Hresh explanation")
            else:
                review = page.get("typographyReview")
                checks = ("referenceCompared", "glyphsCompared", "effectsCompared", "textCompared", "thumbnailCompared")
                if not isinstance(review, dict) or any(review.get(key) is not True for key in checks):
                    raise ValueError("Hresh typography requires all manual comparison checks")
                record = review.get("comparisonRecord")
                if not isinstance(record, str) or not record.strip() or not (manifest.parent / record).is_file():
                    raise ValueError("Hresh typography requires an existing comparisonRecord")
                if not (manifest.parent / record).read_text(encoding="utf-8").strip():
                    raise ValueError("Hresh typography comparisonRecord must not be empty")
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


def render(topic, placement_name, pages, publication=None, has_zip=False):
    escape = html.escape
    post = ""
    if publication is not None:
        alternatives = "".join(f'<li>{escape(title)}（{len(title)}字符）</li>' for title in publication["alternatives"])
        warnings = "".join(f'<p>{escape(warning)}</p>' for warning in publication["warnings"])
        tags = escape(" ".join(f"#{tag}" for tag in publication["tags"]))
        body = f'<p>发布正文</p><pre>{escape(publication["body"])}</pre>' if "body" in publication else ""
        post = (f'<section><h2>发布文案（草稿）</h2><p>推荐标题 · {publication["titleChars"]}字符</p>'
                f'<pre>{escape(publication["title"])}</pre>{body}<p>标签</p><pre>{tags}</pre>'
                + (f'<p>备选标题</p><ul>{alternatives}</ul>' if alternatives else "")
                + warnings + '<p><a href="publication.md">查看可复制文案</a></p></section>')
    figures = []
    for page in pages:
        caption = escape(f'{page["label"]}：{page["title"]}')
        figures.append(f'<figure><figcaption>{caption}</figcaption>'
                       f'<a href="{page["image"]}"><img src="{page["image"]}" alt="{caption}"></a></figure>')
    download = '<p><a href="final-images.zip">下载最终原图 ZIP</a></p>' if has_zip else ""
    return '''<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>最终图片顺序</title><style>
*{box-sizing:border-box}body{margin:0;background:#f6f6f3;color:#20252a;font:16px/1.6 system-ui,sans-serif}
main{max-width:600px;margin:auto;padding:24px 16px}h1{font-size:24px}figure{margin:32px 0}
figcaption{margin-bottom:10px;font-weight:600}img{display:block;width:100%;height:auto}
a{color:#2457a0}small{display:block;color:#555}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;background:white;padding:12px;border:1px solid #ddd}
</style><main><h1>''' + escape(str(topic)) + "</h1><p>" + escape(placement_name) + f' · 共{len(pages)}张，按下方顺序使用。</p>' + \
        download + '<small>仅展示选定最终版。复核标记来自输入清单；打包不执行OCR或平台上传验证。</small>' + \
        post + "".join(figures) + "</main></html>"


def check_publication_update(out_dir, pages):
    allowed = {"images", "index.html", "publication.md", "final-images.zip", "process", ".DS_Store"}
    if not out_dir.is_dir() or any(path.name not in allowed for path in out_dir.iterdir()):
        raise ValueError("Publication updates require an existing compact delivery directory")
    for name in ("index.html", "publication.md"):
        path = out_dir / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f"Refusing to replace a non-regular delivery file: {name}")
    image_dir = out_dir / "images"
    expected = {Path(page["image"]).name for page in pages}
    if (not (out_dir / "index.html").is_file() or image_dir.is_symlink() or not image_dir.is_dir()
            or {path.name for path in image_dir.iterdir() if path.name != ".DS_Store"} != expected):
        raise ValueError("Existing delivery images do not match the selected pages")
    for page in pages:
        path = out_dir / page["image"]
        if path.is_symlink() or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != page["sha256"]:
            raise ValueError("Publication-only updates cannot change image content or order")


def build(manifest, out_dir, images_only=False, create_zip=False, update_publication=False):
    manifest, out_dir = Path(manifest).resolve(), Path(out_dir).resolve()
    if out_dir.exists() and not update_publication:
        raise ValueError(f"Output already exists; use --update-publication for copy-only changes: {out_dir}")
    data, pages, placement_name = load_pages(manifest)
    publication = None if images_only else load_publication(data)
    if update_publication:
        if publication is None or create_zip:
            raise ValueError("--update-publication requires publication copy and cannot be combined with --zip")
        check_publication_update(out_dir, pages)
        for page in pages:
            page.pop("_source")
    else:
        # All input and ordering checks happen before creating a delivery directory.
        (out_dir / "images").mkdir(parents=True)
        for page in pages:
            content = page.pop("_source").read_bytes()
            if hashlib.sha256(content).hexdigest() != page["sha256"]:
                raise ValueError("Source changed while packaging; choose a new output directory and retry")
            (out_dir / page["image"]).write_bytes(content)
        if create_zip:
            with zipfile.ZipFile(out_dir / "final-images.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for page in pages:
                    archive.write(out_dir / page["image"], Path(page["image"]).name)
    report = {"schemaVersion": 1, "topic": data.get("topic", "最终图片"),
              "placement": data["placement"], "scope": data["scope"],
              "bodyPageCount": data["bodyPageCount"], "pages": pages}
    if publication is not None:
        report["publication"] = publication
        (out_dir / "publication.md").write_text(publication_markdown(publication), encoding="utf-8")
    document = render(report["topic"], placement_name, pages, publication,
                      has_zip=(out_dir / "final-images.zip").is_file())
    (out_dir / "index.html").write_text(document, encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--images-only", action="store_true",
                        help="Omit publication copy when the user explicitly asks for images only")
    parser.add_argument("--zip", action="store_true", dest="create_zip", help="Also create a final-image ZIP on request")
    parser.add_argument("--update-publication", action="store_true",
                        help="Update copy in an existing compact delivery after verifying unchanged images")
    args = parser.parse_args()
    try:
        report = build(args.manifest, args.out_dir, images_only=args.images_only,
                       create_zip=args.create_zip, update_publication=args.update_publication)
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    print(f'Final delivery: {args.out_dir / "index.html"}')
    for page in report["pages"]:
        print(f'{page["label"]}：{page["title"]} -> {args.out_dir / page["image"]}')
    if "publication" in report:
        print(f'发布标题：{report["publication"]["title"]}')
        if "body" in report["publication"]:
            print(f'发布正文：{report["publication"]["body"]}')
        print("标签：" + " ".join(f"#{tag}" for tag in report["publication"]["tags"]))
        for warning in report["publication"]["warnings"]:
            print(f"Warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
