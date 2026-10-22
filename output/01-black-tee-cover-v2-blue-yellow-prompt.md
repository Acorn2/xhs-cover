# 黑色T恤封面：蓝黄字体版

- 输出：`01-black-tee-cover-v2-blue-yellow.png`，1086×1448，3:4，小红书图文效果试稿。
- 工具：内置 image_gen，编辑上一版封面。
- 输入1：`01-black-tee-cover-v1.png`，保持人物、背景、构图和文案。
- 输入2：`01-black-tee-cover-v2-color-reference.png`，用户提供的图片，仅参考其中的蓝色与黄色，不参考蓝黄衣着。
- 本版：第一行“用 AI”亮蓝，第二行“把想法做成产品”明黄，保留深色字效与细白边；移除原有黄色装饰短线。
- 已目视检查：主标题及辅助文案完整；黑色圆领短袖、人物脸部与手绘质感保留；无账号名称与署名；低饱和摄影场景保留。颜色为模型依参考图生成，未做像素级色值匹配；生成编辑不保证其他像素完全不变。
- 待确认：标题仍较满，标签箭头仍指向肩部。用户审美确认与平台上传展示尚未完成。

后续确认：用户已认可本版并指定为后续标准，原图的同字节副本保存于 `../atutun-xhs-cover/assets/hresh-cover-approved.png`。标题边距、箭头指向仍按新选题重新检查，不要求复现本图中的偏差；平台上传展示尚未检查。

## 实际编辑提示词

```text
Use case: precise-object-edit
Asset type: revised Xiaohongshu 3:4 cover.
Input image 1 is the COVER TO EDIT. Input image 2 is ONLY a color reference for the bright blue and vivid yellow. Do NOT copy the blue jacket/yellow undershirt, face, composition or text of input image 2.
Make a typography-color revision of INPUT IMAGE 1:
1. Change ONLY the visible face/fill color of the top headline "用 AI" from pale lemon yellow to the rich BRIGHT COBALT / ROYAL BLUE seen in the jacket and check marks of input image 2. Match that saturated medium-bright blue, not cyan, not navy, not pastel. Preserve all glyph shapes and exact text, their dark contours, compact shadows and clean thin white outer edge.
2. Change ONLY the visible face/fill color of the second headline "把想法做成产品" from white to the vivid WARM GOLDEN / SUNFLOWER YELLOW used in the question headline of input image 2. Match that saturated yellow, NOT pale lemon, NOT cream, NOT orange. Preserve all eight Chinese characters, size, positions and readable glyph spacing. Keep dark outlines, compact dark shadow and thin white outer edge.
3. Remove the few small decorative yellow ray marks around the title and hand from input image 1, filling their areas naturally with the existing photographic background. Yellow and blue should concentrate in the typography. Keep the existing off-white paper note and black note text, without extra colored decorations.
KEEP EVERYTHING ELSE from input image 1 essentially unchanged: same recognizable adult illustrated man's face, expressive slightly open mouth, dark tousled hair with subtle blue highlights, slight stubble, matte plain BLACK CREW-NECK SHORT-SLEEVED T-SHIRT, bare arms, pose and anatomy. NO blue jacket, hoodie or yellow undershirt. Keep the same crayon/colored pencil figure texture, irregular dark outline and white sticker contour, never convert him into a photographed person or 3D.
Preserve the same low-saturation warm taupe/gray-brown photographic workspace, softly blurred shelves and plants, left window daylight, lamp, laptop, pale wood desk, notebook and main layout. No new blue background, no blue wash, no new yellow wall. Background must recede and remain low contrast.
Preserve exact visible texts: "用 AI", "把想法做成产品", and "需求 → 设计 → 开发" on the existing small off-white note. Preserve the existing arrow. No added text, signature, Hresh, 赫什, account name, logo or watermark.
Keep exact portrait 3:4 canvas, do not crop, add margins, change composition, split panels or produce a comparison board.
Visual color roles: bright blue = first headline; vivid yellow = second headline; matte black = shirt; muted taupe/gray-brown = scene; warm skin = face and hands.
```
