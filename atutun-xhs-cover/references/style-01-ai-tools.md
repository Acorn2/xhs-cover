# 第01款：AI工具 / 太狠了！

本例用于验证真实工作场景、厚实标题和前景遮挡的组合。用户提供的人物与风格参考仅在本次会话中使用，未包含在仓库中；复用时需提供对应图片。本文件记录实际生图及文字补正提示词，色号为目标颜色，需以输出视觉检查为准。

```text
Use case: ads-marketing
生成一张全新的3:4竖版小红书封面，目标尺寸1536×2048。真实摄影人物与手工漫画贴纸标题结合，输出单张完整封面，不是模板展示页。

参考图1是八款模板合集，仅用其中黑发、黑框眼镜、黑色上衣人物保持身份，不沿用合集的网格、标题框、页眉和编号。参考图2是精美单张封面，参考其宽厚标题、真实工作室摄影、白色人物描边和前后遮挡关系，同时保持该人物五官。重新生成新的工作室画面和排版细节，不直接返回或简单放大参考图2。

场景：一个有真实空间纵深的创作者工作室，左后方窗户有柔和冷色自然光，右后方是虚化的书架、暖色台灯，右侧后方有一块显示深色软件界面的屏幕。画面下方为木质桌面，右下方一台深灰色笔记本电脑从底边自然进入画面，左下方少量书本，封面和书脊不添加文字或品牌。背景适度虚化，保留真实光线和环境层次。前景电脑与书本局部遮挡人物下部躯干。

标题原文只写两行，第一行“AI工具”，第二行“太狠了！”。顶部标题区域占画面高度约40%，最长一行宽约画面90%，保留外轮廓安全边距。使用极宽厚的综艺漫画黑体，大字紧凑，第二行略微错位，整体有轻微上扬的动势。第一行填充柔和浅黄色 #FDFFA7，第二行白色。字效由内到外是填充、粗黑描边、向右下偏移的厚实黑色硬阴影、细白色外轮廓；字面宽厚、字间紧凑、笔画间隙清楚，呈现有厚度的定制标题贴纸。标题直接叠在真实场景上，不使用黑色圆角大底板。第二行下面有一道 #FDFFA7 手绘笔刷划线。

人物居中偏下，保持参考人物的脸型、黑色凌乱短发、黑框眼镜和黑色上衣。面对镜头，眼睛睁大、张嘴惊讶，双手打开在胸前和脸部两侧，手指自然清楚。头部上缘紧接标题下缘，脸部位于画面中部，肩胸和身体向画面下部自然延展，不能以一条水平抠图边截断。面部皮肤、发丝、眼镜和黑衣织物保留清晰摄影纹理，脸部清晰、背景柔和。沿人物外轮廓加干净的白色贴纸描边，头发处保留细微起伏，不用大面积黄色光晕。标题不挡眼睛和嘴巴。

人物左侧肩部空隙，放四张小巧的白色手绘纸贴，自上而下分别写“写作”“做图”“编程”“搞定”，最后一张旁边有一个绿色勾。标签黑色粗手写字、轻微错位旋转，局部 #FDFFA7 短划线。人物右肩上方放一个白色手绘气泡，写“效率翻倍！”，有 #FDFFA7 下划线，一根白色手绘弯箭头指向右后方软件屏幕。两侧少量 #FDFFA7 表情强调短线，增强惊讶感。所有标签都比主标题小得多，不盖住脸和关键手势。

主次顺序是巨大标题、人物表情、能力标签与气泡，背景与前景物件提供真实场景。整体紧凑、明亮、精致，浅黄与白色文字、白色人物描边和冷暖摄影背景统一。所有黄色以 #FDFFA7 为目标，不改成荧光黄或金黄。仅出现指定标题及五组辅助文字，禁止模板序号、ATUTUN / XHS COVER、展示页眉、水印、无关文字、空白占位卡片、规则科技网格和黑色圆角大标题框。
```

## 本次测试与文字补正

2026-10-21 使用内置 imagegen 生成，首版主标题漏了末尾感叹号，随后以首版图片为编辑目标执行以下补正。最终输出为 1086×1448，比例为3:4，未达到提示词中的目标像素尺寸；未强制放大。已目视核对标题及辅助文字、脸部无遮挡、真实场景及前景遮挡。该结果使用了风格参考，尚未验证仅凭文字的还原能力。

```text
Edit the provided generated cover with ONE precise typography correction only. Keep the existing photo, person identity and expression, hands, lighting, room, desk, books, laptop, all label positions, title lettering style and other text unchanged. The main headline is intended to read first line “AI工具”, second line “太狠了！”. It currently omits the final exclamation mark on the second line. Add a clearly visible large white exclamation mark “！” immediately to the right of “了”, matching the main headline’s thick black stroke, black lower-right extruded hard shadow and thin white outer border. Fit it within the canvas safe margin by slightly tightening ONLY the second line if necessary. Keep “AI工具” unchanged and leave the smaller “效率翻倍！” callout unchanged. Preserve the 3:4 vertical format. Do not regenerate the scene or add any other elements.
```
