# 小仓配图 Skill · 小红书封面

- 目标：宣传小仓怪诞正文配图这一开源 Codex Skill，让写作者看懂用途与画风。
- 平台：xhs-note，小红书图文；3:4，目标 1080×1440；5% 基础边距为项目设计预设。
- 风格：09 极简知识专栏风；产品角色为主体，无人物出镜、无个人署名。
- 文案：开源 · Codex Skill / 我做了个 / 文章配图 Skill / 把文章观点，画成具体动作 / 小仓怪诞正文配图。
- 事实来源：/Users/ankanghao/ai_code/xiaoyuehan-illustrations/docs/知乎宣传文稿.md；/Users/ankanghao/ai_code/xiaoyuehan-illustrations/README.md。
- 参考素材：/Users/ankanghao/ai_code/xiaoyuehan-illustrations/examples/images/05-information-well.png，仅用于小仓身份、手绘画风与提取资料动作；新封面不是原始样例截图。
- 执行：内置 image_gen；不调用 Skill 安装指令，不发布。
- 事实边界：开源的是规则与工作流，实际生图依赖运行环境的图像模型及额度；封面不声称免费生图或保证效果，也不暗示任何创作者背书。

## 最终生成提示词

成品：`output/xiaocang-skill-xhs-20261021-v1/cover.png`。实际尺寸 1086×1448，精确 3:4，保留生成原尺寸，未拉伸。

检查状态：`reviewed`（仅本地目视）。已查看生成整图与 225×300 缩略图：标题、辅助文案及产品名准确；主体动作明确，关键物件完整，缩略图可辨认主题与小仓。未做小红书实际上传与展示入口检查，未发布；不声称点击率效果或全部平台适配。

项目检查：10 项 unittest 通过；quick_validate.py 返回 Skill is valid；git diff --check 通过。未修改 Skill 实现或用户既有改动。

```text
undefined
```

