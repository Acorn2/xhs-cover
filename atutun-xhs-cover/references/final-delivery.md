# 最终图片交付：顺序与唯一版本

交付单张成品、正文系列或整组图文前，先完成人工复核，再运行 `scripts/package_images.py`。每个平台单独一份清单和一个交付目录。提示词方案和风格候选比较不走最终打包；候选仍使用预览工具，不把候选集称为发布顺序。

## 明确选择最终版本

规划时给每页指定稳定的阅读顺序；生成、重试、修图不会增加新的逻辑页。修订封面仍占原来的封面页，只更换该页清单中的图片路径。历史文件保留在原处，不扫描目录或依据生成时间、文件修改时间、`v2` 后缀猜测最终版本。

只在实际查看图片后填写 `reviewStatus: reviewed`，最终选定版本填写 `status: final`。它们是人工检查声明，脚本不能判断图片文字、画风或是否真的被看过。

## 交付输入

在任务目录保存独立的 `delivery-input.json`，不要把预览工具的 `variants` 当作交付清单。示例是两页整组的结构，图片路径须替换为本次实际文件，正文数量须与页计划一致：

```json
{
  "schemaVersion": 1,
  "topic": "本次图文主题",
  "placement": "xhs-note",
  "scope": "set",
  "bodyPageCount": 1,
  "pages": [
    {
      "order": 1,
      "role": "cover",
      "title": "封面标题",
      "image": "xhs-note/cover-v2.png",
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

- `placement`：`xhs-note` 或 `douyin-note`，每份只对应一个平台。
- `scope`：`cover` 仅封面；`body` 仅正文；`set` 封面加正文。
- `bodyPageCount`：页计划中的正文数量，不包含封面；`cover` 必须为0，其他范围必须为正整数。
- `order`：最终发布顺序，从1连续编号。数组可乱序，脚本按此字段排序；不能用排序掩盖重复编号或缺页。
- `role`：`cover` 或 `body`。整组及只做封面时必须恰好一张封面且排第一；只做正文时不得出现封面。
- `image`：相对清单目录或绝对本地PNG路径。原图须符合平台3:4比例，实际像素原样保留；重复文件内容即使改名也会被拒绝。
- 只有明确选定且标记已复核的页面能进入清单；不加入初版、候选、主题参考、缩略图或历史修订。脚本不依据文件名识别语义，不能把历史文件误标为最终版后指望它自动分辨。

## 执行与产物

从仓库根目录执行；安装后使用 Skill 目录内的同名脚本。输出目录须不存在，重复制作另用版本目录，不覆盖已交付产物：

```bash
python3 atutun-xhs-cover/scripts/package_images.py \
  --manifest output/<topic-slug>/delivery-input.json \
  --out-dir output/<topic-slug>/final
```

脚本先校验清单和全部输入，输入不合法时以退出码2拒绝打包，不创建交付目录。成功输出：

```text
final/
├── images/
│   ├── 01-cover.png
│   └── 02-body-01.png
├── final-images.zip
├── index.html
├── delivery.json
└── delivery.md
```

只做正文时从 `01-body-01.png` 开始。文件名前缀是发布顺序，`body-01` 是正文内部页序，两者在整组中相差一页。PNG内容不改写；ZIP按同一顺序写入且仅含清单选定的最终图。HTML每张只显示一次，均标明“第N张 · 封面/正文NN”。JSON记录顺序、尺寸和内容摘要，Markdown提供顺序链接，三者使用同一份经校验页表。

## 回复与过程图

最终回复以生成的 `delivery.json` 为唯一图片顺序来源，明确总张数、唯一封面与各正文页，并链接顺序总览、原图包。需要内联展示时也按这份清单展示，每张最终图只列一次；路径使用交付目录中统一编号的PNG，不能回指历史版本。不得只给散图、生成目录或未说明先后顺序的文件列表。

生图工具可能自动展示中间版本，其展示时序由客户端决定，打包脚本无法隐藏或重排这些工具消息。生成前说明过程图不代表最终顺序；发生修订时说明替换的逻辑页，最终仍提供完整顺序总览，不把两个版本当成两张发布图。

打包不执行OCR、视觉复核、平台适配转换或上传，不能把结构校验成功说成内容或平台展示已自动验收。
