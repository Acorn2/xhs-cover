# 01大字压顶风：黑色T恤版封面

- 原图：`01-black-tee-cover-v1.png`，1086×1448，3:4，小红书图文效果试稿。
- 工具：内置 image_gen；独立生成新封面，旧版本保留。
- 参考图1：`../atutun-xhs-cover/assets/hresh-character-black-tee.png`，人物身份、黑色圆领T恤与手绘画风。
- 参考图2：`01-black-tee-cover-v1-style-reference.png`，用户提供的“AI工具 / 太狠了”图片，仅参考摄影场景、光线、层次与浅黄/白色标题；不复用其中的人物身份、文案与效果主张。
- 配色分工：浅黄与白色标题；黑色服装；低饱和灰棕场景；辅助标签黑白。
- 已目视检查：三个文案字符串完整，上衣为黑色短袖，无账号名称与署名，人物保留短发、胡茬与蜡笔质感。背景为生成的摄影质感场景，不是用户真实工作室。
- 偏差与待确认：生成模型额外加入了少量黄色强调短线，标签箭头指向人物肩部而非笔记本，标题外轮廓仍靠近左右边缘。未做精确区域检测或平台上传展示检查，用户审美确认待反馈。

## 实际生成提示词

```text
Use case: ads-marketing
Asset type: Xiaohongshu image-post cover, style 01 oversized headline pressing down, black T-shirt character revision.
Create ONE finished new portrait cover, exact 3:4 ratio, target 1080 x 1440 or higher exact 3:4. Not a mockup, not a comparison board.
INPUT REFERENCE: attached black-T-shirt character illustration is the sole human identity reference. Preserve the SAME adult man's recognizable face, dark tousled short hair with subtle blue streaks, light stubble, eyebrows and natural skin tone. He wears ONLY a PLAIN MATTE BLACK ROUND-NECK SHORT-SLEEVED T-SHIRT, no outer jacket, no yellow undershirt, no garment logos or graphics. Maintain the hand-drawn crayon/colored-pencil figure, uneven dark outlines, soft restrained shadows and white sticker-like outer contour. Do not change him to a photograph, teenager, smooth vector or 3D model.
CONTENT: AI-assisted independent product making, no fabricated metrics or results.
LAYOUT: use strong cover hierarchy, large two-line Chinese headline occupying approximately upper 36-40 percent. Exact line 1 "用 AI"; exact line 2 "把想法做成产品". First line PALE soft lemon yellow #FDFFA7, second line WHITE. Both use broad thick Chinese display letters, tight but readable spacing, a compact heavy dark contour, moderate black hard offset shadow, and thin clean white outer outline. No exaggerated giant extrusion. Keep all text including outlines comfortably 6 percent inside canvas edges. The second line contains eight Chinese characters; fit it completely as a clearly readable single line without stretching or omitting any character. First line somewhat narrower and centered, second line broad. Slight irregular dynamic alignment, no solid rounded headline panel.
CHARACTER: medium-large upper body center/lower area, head just below headline, no overlap over eyes or mouth. New pose: leaning slightly toward an open neutral gray unbranded laptop entering bottom right, his right hand open presenting the note at middle-left, left hand resting near keyboard. An engaged adult expression, eyebrows slightly raised and mouth subtly open as if explaining, not grotesquely shocked. Face and hands are the focal point of the person; the black shirt is a calm nearly neutral mass, with a few charcoal-gray fabric folds. Do not tint shirt blue or introduce yellow clothing.
BACKGROUND: believable photographic-style softly focused home workspace with real perspective, layered depth, natural daylight through a window at left, a very dim warm task lamp and sparse shelves at right. Restrained neutral charcoal, warm taupe, gray-brown and pale wood, overall low saturation and softer detail. This is a GENERIC GENERATED SCENE, not the user's actual studio. The illustrated figure is intentionally composited onto this quiet realistic environment. Background should recede substantially compared with headline and character face. No broad blue field, no blue wall, no yellow color wash, no neon, no huge saturated foliage. Small neutral objects only; avoid decorative colored objects.
FOREGROUND: a pale natural wood desk enters from bottom, with the neutral-gray laptop partly occluding lower torso, a single notebook or small stack of papers to left. No product brand, no legible fake screen content.
SECONDARY TEXT: one SMALL off-white hand-cut paper note at character's left shoulder, with exact dark handwritten text "需求 → 设计 → 开发". Fine dark contour only, no yellow fill or yellow underline. Optional one small white curved arrow from note toward laptop, with dark edge for readability. No other cards, badges, stickers or accent bursts. Main headline is the only strong yellow element.
PALETTE ROLES: pale lemon yellow/white = main typography; matte black = clothing; low-saturation taupe/gray-brown = environment; natural warm skin = face and hands. Tiny blue highlights in HAIR ONLY as identity reference, no blue garment or decorative blue. Paper note black/white.
ONLY render these exact visible strings: "用 AI", "把想法做成产品", "需求 → 设计 → 开发". NO account names, Hresh, 赫什, signature, watermark, template numbers, additional words, logo or platform UI. Preserve natural hand anatomy and readable Chinese. Make all hierarchy, saturation and texture contrasts deliberate: typography first, face/expression second, small note third.
Input image 2 is the user's photographic "AI工具 / 太狠了" cover reference. Use it ONLY for the low-saturation realistic workspace, layer separation, lighting, and pale-yellow/white title color hierarchy. Do NOT copy its real person's face or turn the illustrated character into that person. Do NOT copy its wording, logos or performance claims. Character identity and black T-shirt are exclusively from input image 1. Render only the three exact strings specified above.
```
