# 最终图片交付：顺序与唯一版本

交付单张成品、正文系列或整组图文前，先完成人工复核，再运行 `scripts/package_images.py`。每个平台单独一份清单和一个交付目录。提示词方案和风格候选比较不走最终打包；候选仍使用预览工具，不把候选集称为发布顺序。

## 明确选择最终版本

规划时给每页指定稳定的阅读顺序；生成、重试、修图不会增加新的逻辑页。修订封面仍占原来的封面页，只更换该页清单中的图片路径。候选与历史版本留在工作目录，不扫描目录或依据生成时间、文件修改时间、`v2` 后缀猜测最终版本。

默认每个平台只有一个最终交付目录：单平台直接使用 `output/<topic-slug>/`，双平台分别使用其下的平台 ID 目录。最终目录只放统一编号图片、`index.html` 和有文案时的 `publication.md`；不追加 `final/`、`final-with-publication/` 或重复 README。ZIP仅在用户需要下载包时生成。

页计划、来源路径、完整提示词及简短复核记录集中在 `.tmp/<topic-slug>/work.md`；交付输入保存在同一工作目录。原始材料默认引用，不复制；每页提示词只保存一份，不再同时输出 `pages.json` 和 `prompts/`。生成原图、修订和检查报告也留在该工作目录。用户明确要可复现资料时，才将必要资料整理到最终目录的 `process/`，不复制最终原图和可重建预览。

只在实际查看图片后填写 `reviewStatus: reviewed`，最终选定版本填写 `status: final`。它们是人工检查声明，脚本不能判断图片文字、画风或是否真的被看过。

所有成品按 [公开内容边界](../SKILL.md#公开内容边界不展示网址不刻意引导)验收：逐张查看封面、正文、总结页及截图、页脚、背景边角，不含网址、域名、二维码、联系方式和引流/互动引导；推荐标题、备选、发布正文、标签及按需提供的评论草稿也逐项检查。来源链接仅在内部 `work.md`，署源可用名称、文献标题或年份，本地图片与交付入口链接不受影响。将实际查看的图片、文案和检查结论记入工作记录；发现残留时先修正并复核，不得填 `reviewed`、`final` 或打包为成品。只补文案时指出既有图片的问题，不擅自重新生图，也不声称整组已通过。打包脚本不做OCR、网址或引导语义检测，执行成功不等于此项通过。

新制或重制Hresh封面时，先按 [人物要求](../SKILL.md#hresh-封面人物要求)验收：已确认角色必须实际出现，身份与母版一致，在原图和缩略图中清楚可辨。将实际传入的人物母版、效果参考、查看的成品路径及目视结论记入 `work.md`；用户明确要求无人物或替换角色时，记录其原始指令，并按该例外复核。没有明确例外而缺人物、角色错误或未完成复核时，先修正，不得填写 `reviewed`、`final` 或打包为成品。预览或打包成功不能替代此检查；只补发布文案时不据此重新生图或改变既有图片。

新制或重制Hresh封面还必须按[标题字形与字效强制验收](virtual-character.md#标题字形与字效强制验收)将最终图与参考图并排核对，逐项写入 `work.md`；使用下述版本2字段。脚本只能检查人工声明和记录文件存在，不能判断字体像不像、记录是否真实或用户是否认可。

## 交付输入

在 `.tmp/<topic-slug>/delivery-input.json` 保存独立交付清单，不要把预览工具的 `variants` 当作交付清单。示例是两页整组的结构，图片路径相对清单目录，须替换为本次实际文件，正文数量须与页计划一致：

```json
{
  "schemaVersion": 2,
  "topic": "本次图文主题",
  "placement": "xhs-note",
  "scope": "set",
  "bodyPageCount": 1,
  "publication": {
    "title": "给文章配图，我给AI立了条规矩",
    "alternatives": ["文章配图，别再拿灯泡糊弄我了", "我把文章配图规则，做成了开源Skill"],
    "body": "给文章配图时，先圈出读者最容易卡住的地方，再决定画什么。比如文章在讲两个步骤怎么衔接，配图就把输入、动作和结果画出来，让人顺着图看懂中间发生了什么。",
    "tags": ["文章配图", "AI工具", "内容创作", "开源项目"]
  },
  "pages": [
    {
      "order": 1,
      "role": "cover",
      "title": "封面标题",
      "image": "xhs-note/cover-v2.png",
      "typographyStandard": "hresh-confirmed",
      "typographyReview": {
        "referenceCompared": true,
        "glyphsCompared": true,
        "effectsCompared": true,
        "textCompared": true,
        "thumbnailCompared": true,
        "comparisonRecord": "work.md"
      },
      "status": "final",
      "reviewStatus": "reviewed"
    },
    {
      "order": 2,
      "role": "body",
      "title": "正文第一页标题",
      "image": "xhs-note/body-01.png",
      "status": "final",
      "reviewStatus": "reviewed"
    }
  ]
}
```

- 新交付优先使用 `schemaVersion: 2`；版本1仍可读取，供历史清单兼容，不得用版本1规避新制Hresh封面的复核。
- 版本2的每张封面必须填写 `typographyStandard`。Hresh默认填 `"hresh-confirmed"`，并填 `typographyReview`：`referenceCompared`、`glyphsCompared`、`effectsCompared`、`textCompared`、`thumbnailCompared` 均为 `true`，另填 `comparisonRecord` 指向实际 `work.md` 文件。只有已完成对应人工核查时才可填 `true`。非Hresh封面或用户明确指定其他标题风格/无字时填 `"other"`，并在 `typographyException` 记非Hresh或用户明确的原话；人物例外不自动取消标题要求。
- `placement`：`xhs-note` 或 `douyin-note`，每份只对应一个平台。
- `scope`：`cover` 仅封面；`body` 仅正文；`set` 封面加正文。
- `bodyPageCount`：页计划中的正文数量，不包含封面；`cover` 必须为0，其他范围必须为正整数。
- `publication`：整组默认必填，写法见 [发布文案规则](publication-copy.md)。`title` 是推荐发布标题，`alternatives` 为备选字符串数组，`body` 为可直接发布的简短正文，`tags` 为非空、无重复的标签数组；脚本记录实际字符数并统一处理前导 `#`。`pages[].title` 仍是图片内预期文字，二者独立。新做整组时默认填写 `body`。为兼容历史清单及仅补标题或标签的任务，脚本允许省略 `body`，提供时必须是非空字符串。
- 小红书自动生成的推荐及备选发布标题采用不超过20字符的编辑预算；不是已核实的上传限制。用户锁定原文时填 `publication.titleLocked: true`，即使超预算也保留原文并记录提醒。锁定稿不要求另写备选；抖音只记录长度，不写死未经验证的上传限制。
- `order`：最终发布顺序，从1连续编号。数组可乱序，脚本按此字段排序；不能用排序掩盖重复编号或缺页。
- `role`：`cover` 或 `body`。整组及只做封面时必须恰好一张封面且排第一；只做正文时不得出现封面。
- `image`：相对清单目录或绝对本地PNG路径。原图须符合平台3:4比例，实际像素原样保留；重复文件内容即使改名也会被拒绝。
- 只有明确选定且标记已复核的页面能进入清单；不加入初版、候选、主题参考、缩略图或历史修订。脚本不依据文件名识别语义，不能把历史文件误标为最终版后指望它自动分辨。

## 执行与产物

从仓库根目录执行；安装后使用 Skill 目录内的同名脚本。首次输出目录须不存在。重新制图先明确归档旧交付，再建立唯一的新交付入口，不静默覆盖，也不不断追加平级“最终版”：

```bash
python3 atutun-xhs-cover/scripts/package_images.py \
  --manifest .tmp/<topic-slug>/delivery-input.json \
  --out-dir output/<topic-slug>
```

用户明确只要图片时追加 `--images-only`，脚本会跳过并忽略 `publication`，只生成图片交付。旧版不含文案的整组清单可在该模式下继续使用；默认整组缺少标题或标签会在创建输出目录前失败。只做封面或只做正文不强制带 `publication`，提供时仍需通过文案校验。

脚本先校验清单和全部输入，输入不合法时以退出码2拒绝打包，不创建交付目录。成功输出：

```text
output/<topic-slug>/
├── images/
│   ├── 01-cover.png
│   └── 02-body-01.png
├── index.html
└── publication.md
```

只做正文时从 `01-body-01.png` 开始。文件名前缀是发布顺序，`body-01` 是正文内部页序，两者在整组中相差一页。PNG内容不改写；HTML每张只显示一次，均标明“第N张 · 封面/正文NN”。需要压缩包时在首次命令追加 `--zip`，按同一顺序输出仅含最终图片的 `final-images.zip`，HTML仅在存在ZIP时显示下载链接。

带 `publication` 时输出 `publication.md` 可复制草稿，HTML同时显示推荐标题、备选、发布正文和标签（按清单提供的字段）。仅图片模式不产生文案文件。不再输出 `delivery.json` 或 `delivery.md`；校验结果由脚本返回并在终端列出页序，不另存一份同内容清单。打包只校验文案结构与编辑预算，不能判断标题是否会有传播效果。

只补发布文案时，修改原交付输入的 `publication`，在同一命令追加 `--update-publication`。脚本先核对最终图片集合、字节内容及页序全部一致，再更新原目录的 `publication.md` 和 `index.html`，不复制图片或重建ZIP；可为先前的纯图片交付补文案。不能与 `--zip` 同用；图片变化或目录含未知文件时拒绝更新，避免覆盖其他资料。不要另建 `final-with-publication`。工作清单已不存在时，可按编号图片与HTML中的页序重建，须实际复核；不在每次正常交付额外保存备份清单。

## 回复与过程图

最终回复以脚本校验并输出的页序为准，明确总张数、唯一封面与各正文页，链接 `index.html`；仅在已生成ZIP时链接原图包。需要内联展示时也按此顺序，每张最终图只列一次；路径使用交付目录中统一编号的PNG，不能回指历史版本。不得只给散图、生成目录或未说明先后顺序的文件列表。

整组还需直接给出推荐发布标题、简短发布正文、标签与备选，和清单保持一致，不只给附件入口。发布文案均为草稿，不表示已发帖；用户明确只要图片时省略这些字段。

生图工具可能自动展示中间版本，其展示时序由客户端决定，打包脚本无法隐藏或重排这些工具消息。生成前说明过程图不代表最终顺序；发生修订时说明替换的逻辑页，最终仍提供完整顺序总览，不把两个版本当成两张发布图。

打包不执行OCR、视觉复核、平台适配转换或上传，不能把结构校验成功说成内容或平台展示已自动验收。
