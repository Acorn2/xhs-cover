# 第二版：减轻背景

- 输出：`01-virtual-character-v2.png`，1086×1448，3:4，小红书图文效果试稿。
- 工具：内置 `image_gen`，编辑第一版；第一版保留。
- 输入1：`01-virtual-character-v1.png`，编辑目标。
- 输入2：`../atutun-xhs-cover/assets/hresh-character.png`，人物身份与笔触母版。
- 修改重点：去掉大面积蓝色背景，改为暖米白纸底与低对比浅灰线稿，缩小标题、减轻黑色字效。
- 已目视检查：标题、辅助文字、署名保留，角色服装与脸部一致，背景大面积蓝色已移除。生成结果仍保留少量蓝黄装饰线、前景书本和较粗箭头，未完全执行提示词中的简化要求。审美效果待用户反馈，未检查平台上传展示，未生成抖音版。

## 实际编辑提示词

```text
Use case: precise-object-edit
Asset type: revised Xiaohongshu 3:4 cover, version 2.
Input image 1 is the cover to edit. Input image 2 is the original fixed character identity and drawing-style reference.
The user dislikes the overwhelming saturated blue background. Edit the COVER to make the background much lighter, quieter and more spacious. This is primarily a background and visual-weight correction. Keep the same exact texts, layout relationship, recognizable adult character identity, face, dark tousled blue-highlighted short hair, light stubble, blue hooded jacket, yellow shirt, pose, laptop, and crayon/colored pencil hand drawing. Do not turn the character into a photo or different person.
Replace ALL large saturated blue backdrop areas, shelves, and dark busy room textures with warm off-white/ivory #FFF9EC paper. At least 80 percent of the BACKGROUND behind text and character should be plain warm off-white paper with subtle visible grain. Do NOT add any blue rectangle, blue color field, blue brush wash, blue gradient, cyan area, or substitute other saturated color blocks. Blue should be concentrated on the character's jacket, with only a few fine muted blue-gray sketch strokes elsewhere.
Very sparse, low-contrast pale warm-gray pencil outlines may suggest one shelf and one unlit desk lamp behind the character. No filled shelf wall, no scattered decorative stroke bursts, no dark room panel, no yellow light beam. Background must recede and leave lots of empty off-white paper.
Retain the same principal headline text exactly, with two lines:
"用 AI"
"把想法做成产品"
Retain clear bold Chinese lettering; yellow first line, off-white second line. REDUCE the excessive black outline and black extrusion thickness by about half, preserve clear readable dark outlines with a compact hard shadow. Gently reduce the total headline width enough to keep all outer edges inside 5 percent margins. Do not change any text. Do not add a black title panel.
Retain the single white paper card with exact text "需求 → 设计 → 开发", with readable blue handwriting. Keep one simple thin muted blue arrow from this card toward laptop, no decorative marks.
Preserve natural character face and anatomy from input 2; same adult, not a teenager. White sticker outline around the figure can be a little finer against light paper. Keep hands natural and the same pose.
Keep foreground laptop unbranded gray, desk in pale natural warm neutral crayon with lighter sparse shading. Simplify extra foreground books and pen cup so they do not dominate. Keep exact signature "Hresh赫什", ensuring clear correct Chinese characters.
Only visible texts: "用 AI", "把想法做成产品", "需求 → 设计 → 开发", "Hresh赫什".
Color palette is warm ivory background, cobalt-blue jacket, warm-yellow shirt/headline accent, neutral gray laptop, deep outlines and natural skin/hair. No decorative red, green, pink, purple.
Overall: clean, warm, restrained hand-drawn creator cover, character vivid against a quiet light paper backdrop. Maintain a strict 3:4 portrait ratio, not a framed mockup. No watermark or additional text.
```
