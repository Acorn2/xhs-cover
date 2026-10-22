# 第三版：去掉账号署名

- 输出：`01-virtual-character-v3.png`，1086×1448，3:4，小红书图文效果试稿。
- 工具：内置 `image_gen`；编辑目标：`01-virtual-character-v2.png`。
- 修改：去掉左下角账号署名及其黄色划线，以桌面纹理补齐，保留第二版的浅色背景和构图。
- 已目视检查：左下角无账号名称与划线；主标题和辅助文案完整，主要构图保留。生成编辑存在局部笔触差异，不承诺其他像素完全相同。尚未检查平台上传展示，未生成抖音版。

## 实际编辑提示词

```text
Use case: precise-object-edit
Edit the provided cover image with ONE localized change only: remove the handwritten account signature "Hresh赫什" located in the LOWER LEFT CORNER of the image, together with its short yellow underline. This text is the user's own account label and the user explicitly requests its removal.
Seamlessly fill ONLY that small signature/underline region with the surrounding light warm ivory and pale ochre crayon desk/paper texture. Do not replace it with other text or symbols.
Preserve the entire rest of the image exactly: same 3:4 canvas and resolution, same warm off-white background, fine gray background shelves and lamp, same character identity, facial expression, hair, blue jacket, yellow shirt, same hands and pose, same laptop, desk, books, pen cup and arrow. Preserve the existing positions, sizes, outlines, colors and crayon grain. No layout redesign, no extra margins or new elements.
Keep the main headline exactly "用 AI" and "把想法做成产品". Keep the small card text exactly "需求 → 设计 → 开发".
Only these three content text strings may remain. No account name, signature, personal logo or account watermark anywhere.
```
