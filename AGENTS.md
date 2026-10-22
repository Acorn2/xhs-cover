# 项目约定

这是一个本地可安装的封面与正文图策划 Skill，保留名称与目录 `atutun-xhs-cover` 以兼容既有调用。主体职责是内容判断、正文拆页、视觉风格选择和平台版位适配；本仓库不提供图片生成 API、发布服务或平台登录。

- `atutun-xhs-cover/SKILL.md` 是入口；风格细节和平台规则放在 `references/`，确定性预览脚本放在 `scripts/`。
- `examples/` 保存已交付图片和可复现示例。原八款图片是3:4视觉样例，不代表其他平台适配成品，不覆盖历史生成记录。
- 平台画布、安全区、标题长度是设计预设，不能写成未经核实的上传限制或算法规则。具体坐标以 `platform-presets.json` 为单一来源。
- 当前只支持小红书图文与抖音图文；生成前分别确定标题、信息密度、视觉锚点与构图。同为3:4也不能通过裁切或改平台名冒充独立生成。
- 封面与正文分别选择模板，正文默认无人物，不继承封面人物母版、配色或材质；一组正文统一主题，各页按内容选择布局。正文规则入口为 `references/body-images.md` 与 `references/body-templates.md`；旧调用未说明范围时保持只做封面。
- 展示检查只用于生图后的验收。抖音视频、公众号、视频号和朋友圈不在当前范围；历史五版位演示存于 `examples/archive/`，不能作为当前能力。
- 没有生成、查看和复核的成品不能标为“已适配”。
- 实际成品交付必须走 `scripts/package_images.py`，详见 `references/final-delivery.md`：按明确页序输出，整组仅一个最终封面；历史版本与候选不进入最终包。预览清单允许多候选，不能替代最终交付清单。
- 运行 `python3 -m unittest discover -s tests -v`、Skill 的 `quick_validate.py` 和 `git diff --check`。预览脚本只依赖 Python 标准库，示例输入为 `examples/platform-preview.json`。
