# 正文视觉风格：8款示例 · 第一套

2026-10-22归档。使用同一份《提需求前的五项清单》测试文案，8种主题独立生成，均为小红书图文3:4正文示例。实际尺寸均为1086×1448，默认无人物；没有为了归档裁切、缩放或改字。

[打开八款总览](index.html) · [生成与复核清单](manifest.json) · [完整复核说明](review.md) · [测试文案](source.md)

本目录展示8款当前样图，保存生成与局部修正提示词、实际参考素材、编辑初稿与版本历史。清爽文档v3与杂志图解v2已获用户确认，作为各自主题的当前版本，[新旧对照](revisions/02-clean-editorial/index.html)保留旧图与中间版。内部素材与记录使用相对路径，整体复制本目录即可浏览并查阅生成输入；原 `output/` 生成记录保留。模型重新生成的结果可能与本套图片存在差异。

| 编号 | 主题 | 原图 | 生成提示词 |
| --- | --- | --- | --- |
| 01 | 清爽文档 `body-clean` · v3 | [PNG](revisions/02-clean-editorial/body-clean-v3.png) | [生成](revisions/02-clean-editorial/prompts/body-clean-v2.md) / [字体精修](revisions/02-clean-editorial/prompts/body-clean-v3-type.md) |
| 02 | 手绘讲义 `body-sketch` | [PNG](body-sketch.png) | [提示词](prompts/body-sketch.md) |
| 03 | 杂志图解 `body-editorial` · v2 | [PNG](revisions/02-clean-editorial/body-editorial-v2.png) | [提示词](revisions/02-clean-editorial/prompts/body-editorial-v2.md) |
| 04 | 清透双色文艺印刷 `body-duotone-print` | [PNG](body-duotone-print.png) | [提示词](prompts/body-duotone-print.md) |
| 05 | 颗粒蜡笔插画 `body-crayon` | [PNG](body-crayon.png) | [提示词](prompts/body-crayon.md) |
| 06 | 清爽数字手绘注解 `body-digital-notes` | [PNG](body-digital-notes.png) | [提示词](prompts/body-digital-notes.md) |
| 07 | 撕纸手绘拼贴 `body-paper-collage` | [PNG](body-paper-collage.png) | [提示词](prompts/body-paper-collage.md) |
| 08 | 黑板粉笔 `body-chalkboard` | [PNG](body-chalkboard.png) | [提示词](prompts/body-chalkboard.md) |

原三款初始生成没有输入参考图；清爽文档新版v3在重新生成的v2基础上精修字体，杂志图解新版重新生成。新增五款使用 `references/` 中各自的风格参考；其第一版在第04项混入头像符号，归档在 `initial-v1/`，只作编辑输入与历史记录。对应修正提示词及输入见 `manifest.json` 的 `correction`，旧清爽与旧杂志记录见 `history`。

用户此前明确偏好手绘讲义，并对新增五款表达正面反馈。本套只覆盖单页清单布局，不代表48种主题与布局组合、抖音适配或平台上传验收完成。图片中的待办工具内容是演示材料，不代表用户真实产品或实测结果。
