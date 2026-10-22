# atutun-xhs-cover

面向**小红书图文与抖音图文**的封面策划 Skill，包含 **12 种视觉风格**。同一份内容先按两个平台分别确定标题、信息密度、视觉锚点与构图，再输出独立生图提示词；展示检查仅用于生图后的验收。

保留名称 `atutun-xhs-cover` 和原安装方式。原八款图片与提示词仍可复用，新流程不再要求固定八轮问答或所有封面都露脸。

01–08延续人物贴纸、大标题和场景纵深的视觉体系，支持真人或固定虚拟人物；Hresh 默认使用下方已确认的黑色T恤、蓝黄标题标准，其他用户可使用原浅黄/白色基础配色或自己的品牌。09–12补充知识专栏、专业科技、生活记录和数据报告风，允许产品或场景成为主体。适合 AI 工具、教程、测评、知识和经验分享。

## 当前支持与生成策略

| 平台 | 制作预设 | 生图前的区别 |
| --- | --- | --- |
| 小红书图文 | 3:4 · 1080×1440 | 突出主题与实用价值，可保留少量步骤、清单或证据 |
| 抖音图文 | 3:4 · 1080×1440 | 一个简短问题/卖点，放大一个视觉主体，减少辅助信息 |

**同为3:4也要分别设计与生成。** 例如同一资料整理主题，小红书可以呈现“流程＋三个步骤”，抖音可以呈现“资料太乱的问题＋清单结果”，不能裁切小红书成品充当抖音版。

这些是可调整的设计策略，非平台唯一审美、上传规格或算法规律。当前不处理抖音视频、公众号、视频号及朋友圈，后续范围见 [ROADMAP.md](ROADMAP.md)。详细规则见 [两平台生成策略](atutun-xhs-cover/references/platform-adaptation.md)。

## 模板效果

### 当前已确认标准

[<img src="atutun-xhs-cover/assets/hresh-cover-approved.png" alt="已确认的黑色T恤、亮蓝明黄标题封面标准" width="420">](atutun-xhs-cover/assets/hresh-cover-approved.png)

Hresh 默认以这张1086×1448（3:4）小红书封面作为视觉参考：**黑色圆领T恤手绘人物、亮蓝第一行与明黄重点行、低饱和摄影背景、黑白辅助信息、无账号署名**。人物身份和视觉效果分别由两张随包素材控制，详细规则见[当前封面标准](atutun-xhs-cover/references/virtual-character.md#当前封面标准)。新选题按平台与模板独立设计，不照抄示例标题、场景或动作；09–12保留各自简洁或证据优先的结构。

仅此张新版已获得用户视觉确认，其他模板和抖音新版尚未按此标准重新生成与检查。完整生成记录保留于[蓝黄字体版提示词](output/01-black-tee-cover-v2-blue-yellow-prompt.md)。

### 历史风格示例

[第一套12款虚拟人物示例](examples/virtual-character-set-01/index.html)使用旧蓝黄服装，保留用于构图对照，不作为当前衣着、标题色或背景材质的默认标准。12张均为1086×1448（3:4），仅为小红书图文示例；[独立目录与说明](examples/virtual-character-set-01/README.md)包含原图、完整提示词、参考素材及复核记录，原八款图片保留。

以下是已生成的01–08风格示例，单张尺寸均为 **1086 × 1448（3:4）**；它们用于展示视觉风格，尚不是按同一主题分别生成的两平台对照成品。点击图片查看原图，也可以查看 [八款总览](examples/overview.png)。

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>01 · 爆款大字压顶风</h3>
      <a href="examples/01-ai-tools.png"><img src="examples/01-ai-tools.png" alt="爆款大字压顶风：AI工具，太狠了！" width="420"></a>
      <p>两行大字与人物紧密衔接，真实场景和前景遮挡增加层次。适合强钩子标题、经验分享和教程入口。</p>
    </td>
    <td width="50%" valign="top">
      <h3>02 · 巨字拆分冲击风</h3>
      <a href="examples/02-giant-word-impact.png"><img src="examples/02-giant-word-impact.png" alt="巨字拆分冲击风：AI实战，效率暴涨" width="420"></a>
      <p>核心词块围绕人物排布，字形、手势和箭头形成动势。适合概念、能力和身份类主题。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>03 · 小白科普问答风</h3>
      <a href="examples/03-beginner-qa.png"><img src="examples/03-beginner-qa.png" alt="小白科普问答风：AI智能体到底是啥？" width="420"></a>
      <p>口语化问题、疑惑表情和问号搭配学习标签。适合解释概念、回答常见问题和零基础科普。</p>
    </td>
    <td width="50%" valign="top">
      <h3>04 · 教程清单风</h3>
      <a href="examples/04-tutorial-checklist.png"><img src="examples/04-tutorial-checklist.png" alt="教程清单风：从0搭建AI专属助手" width="420"></a>
      <p>人物指向侧边步骤，绿色勾选与底部短句突出上手路径。适合安装、部署和全流程教程。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>05 · 产品测评榜单风</h3>
      <a href="examples/05-product-comparison.png"><img src="examples/05-product-comparison.png" alt="产品测评榜单风：主流AI工具到底怎么选，5款实测" width="420"></a>
      <p>巨大数字、产品卡片和指向箭头突出比较主题。适合工具横评、产品榜单和选择建议。</p>
    </td>
    <td width="50%" valign="top">
      <h3>06 · 种草推荐风</h3>
      <a href="examples/06-warm-recommendation.png"><img src="examples/06-warm-recommendation.png" alt="种草推荐风：这5个AI工具真的太香了！" width="420"></a>
      <p>暖色生活场景、微笑点赞和推荐贴纸营造亲切感。适合工具、播客、书籍与资源推荐。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>07 · 贴纸拼贴入门风</h3>
      <a href="examples/07-sticker-beginner.png"><img src="examples/07-sticker-beginner.png" alt="贴纸拼贴入门风：小白也能玩转AI，从0入门！" width="420"></a>
      <p>上下标题包围人物，工具卡片错落分布。适合入门指南、工具组合和工作流搭建。</p>
    </td>
    <td width="50%" valign="top">
      <h3>08 · 黑底效率工作流风</h3>
      <a href="examples/08-dark-workflow.png"><img src="examples/08-dark-workflow.png" alt="黑底效率工作流风：我的AI工作流" width="420"></a>
      <p>深色工作场景、工具墙和绿色清单突出效率收益。适合个人工作法、自动化和工具组合分享。</p>
    </td>
  </tr>
</table>

示例使用 AI 图片生成模型制作，用于展示构图与视觉效果；“5款实测”“效率翻倍”等示例文案不代表实际测评或效果承诺。生成结果会受模型、人物参考图和最终提示词影响。

## 新增四种视觉风格

| 编号 | 风格 | 适合内容 | 视觉重点 |
| --- | --- | --- | --- |
| 09 | 极简知识专栏风 | 系统解释、知识系列、方法论 | 一个概念、稳定对齐、留白与品牌识别 |
| 10 | 专业科技测评风 | 软件、AI工具与数码 | 真实产品/界面证据、理性比较 |
| 11 | 真实生活记录风 | 经历、工作过程与生活 | 自然摄影、真实环境、少量文字 |
| 12 | 数据分析报告风 | 有来源的数据与行业观察 | 单一重点图形、正确单位和事实边界 |

四种风格的规则与提示词骨架已提供，对应图片已纳入[虚拟人物示例集](examples/virtual-character-set-01/index.html)。10为工具概念、11为生成场景、12为无数据的定性流程，不代表真实测评或用户环境照片。参见 [扩展视觉库](atutun-xhs-cover/references/styles-extended.md)。

## 快速开始

将仓库中的 `atutun-xhs-cover` 目录复制到 Codex 的 skills 目录：

```bash
cp -R atutun-xhs-cover ~/.codex/skills/
```

安装后调用：

```text
$atutun-xhs-cover
```

也可以直接说明需求：

```text
$atutun-xhs-cover
这是我的文章：[粘贴正文]
用于小红书图文和抖音图文，均为3:4。
按平台分别确定标题、辅助信息和构图，再给两份完整生图提示词。
可以复用同一风格与配色，但不要裁切同一成品代替两个版本。
```

## 使用流程

只需要五类信息：**内容、平台版位、主体、素材、偏好**。从当前消息提取已知信息，未指定的样式由 Skill 推荐；仅缺少会改变结果的信息时补问。未指定平台时会说明默认小红书图文，无人物方案不强迫上传照片。

主流程是：**内容分析 → 两平台分别制定生成策略 → 组合风格 → 各自完整提示词 → 分别生图 → 事后展示检查**。复用人物身份与品牌配色；用户锁定标题时保留原文，通过主体与辅助信息安排体现区别，不为增加点击虚构数字或效果。

这个 Skill 提供策划、提示词与预览脚本，不包含独立生图服务。用户要求图片时，由当前环境可用的图片工具制作所选版本；只要求提示词时不会自动生图或发布。

### 不露脸：使用固定虚拟人物

为 Hresh赫什制作人物封面时，使用随 Skill 保存的[黑色T恤人物母版](atutun-xhs-cover/assets/hresh-character-black-tee.png)与[已确认效果参考](atutun-xhs-cover/assets/hresh-cover-approved.png)，无需提供真人照片。保持深色短发、浅胡茬、蜡笔质感与白色贴纸边，当前服装为纯黑色圆领短袖；按选题变化表情、动作和构图，用户指定时可独立换装。原蓝黄母版及第一套12款示例保留，未自动重做。产品、场景和无人物方案仍可明确指定；其他用户使用自己的母版。

```text
$atutun-xhs-cover
用内置的 Hresh 虚拟人物，不用真人照片。
内容：[粘贴正文]
用于小红书图文和抖音图文，按各自策略给出完整提示词。
保持人物身份和手绘画风，穿纯黑色圆领T恤，分别安排动作、辅助信息和构图。
按已确认效果参考使用亮蓝/明黄标题与低饱和背景，不加账号署名。
```

01–08可直接采用虚拟人物；09–12根据内容决定是否出现人物，产品截图和数据仍须有真实依据。详见[固定虚拟人物规则](atutun-xhs-cover/references/virtual-character.md)。旧12款已生成并逐张目视检查，新版01视觉方向已获用户确认；新版其他模板与虚拟人物抖音版尚未生成，平台上传展示尚未检查。

## 生图后的检查（可选）

主要检查3:4原图、文字准确性、主体层级、基础边距与缩略图可读性，不生成平台方案或把图片转换成另一平台版本。

<details>
<summary>查看检查脚本与演示</summary>

```bash
python3 atutun-xhs-cover/scripts/preview_covers.py \
  --manifest examples/platform-preview.json \
  --out-dir .tmp/platform-preview-new
```

[检查演示](examples/platform-preview/index.html) · [结构化报告](examples/platform-preview/report.json) · [输入说明](atutun-xhs-cover/references/preview-workflow.md)

演示使用历史PNG，仅说明检查流程。输入区域由人工标注，不做OCR；报告仍需目视复核。目录已存在时换新目录，不覆盖旧结果。此前五版位裁切演示已归档，不作为当前能力。

</details>

## 视觉与事实约定

- 当前两平台均采用3:4，风格不绑定平台；生成目标、标题与信息预算分别决定。
- 01–08的通用模板使用浅黄/白色基础字效；Hresh 默认以已确认效果图的亮蓝/明黄替换原配色。09–12使用自己的视觉结构，人物与品牌偏好不强制改变其信息层级。
- 真人身份来自参考照，虚拟人物身份与画风来自已确认母版；不把虚拟人物写实化，不索要真人照来维持虚拟身份。无人物方案可用产品、环境和概念图，装饰服务于主题。
- 封面默认不添加账号名称、署名、账号水印或个人品牌Logo；使用固定人物不意味着在图片上写账号名称，用户明确要求时才添加。
- “5款”“实测”“零基础”“效率翻倍”等表达须有材料依据；分析图表不编造数值或评分。
- 两平台分别保存生成方案和原图，检查视图不冒充成品。中文标题逐字核对，含标点。
- 可编辑文字需交付真实文字图层或独立文案与布局记录；当前脚本不合成文字、不导出最终位图。

具体规则见 [Skill 入口](atutun-xhs-cover/SKILL.md)、[原八款视觉库](atutun-xhs-cover/references/styles-atutun.md) 和 [第01款历史示例](atutun-xhs-cover/references/style-01-ai-tools.md)。

[完整两平台示例](atutun-xhs-cover/references/multi-platform-example.md)展示同一09知识专栏风在相同3:4比例下，为小红书与抖音图文分别输出生成目标、标题、信息量、构图和最终提示词。

## 目录说明

```text
.
├── README.md
├── AGENTS.md                    # 项目约定与验证入口
├── MVP.md / ARCHITECTURE.md / TECH-STACK.md
├── atutun-xhs-cover/             # 复制此目录安装 Skill
│   ├── SKILL.md                  # 五类输入与两平台生成工作流
│   ├── agents/openai.yaml
│   ├── assets/hresh-character-black-tee.png # 当前默认黑色T恤人物母版
│   ├── assets/hresh-cover-approved.png # 用户已确认的蓝黄字体效果参考
│   ├── assets/hresh-character.png # 原蓝黄母版，保留历史引用
│   ├── references/               # 12种风格、平台预设与预览说明
│   └── scripts/preview_covers.py  # Python 标准库展示检查
├── tests/                       # 预览几何与输入/输出保护
└── examples/                    # 八款原图、生成记录及平台预览
```

`examples/` 供浏览和对照，不需要复制到 skills 目录。历史八款示例的真人与风格参考原图未包含在仓库中；Hresh 当前人物母版与已确认效果参考均保存在 `atutun-xhs-cover/assets/`，随 Skill 一起安装，不依赖 `output/` 或临时附件。其他人物请提供自己的参考图。更多记录见 [示例说明](examples/README.md)。

## 本地验证

```bash
python3 -m unittest discover -s tests -v
git diff --check
```
