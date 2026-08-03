# Lilac Dream 五主题扩展方案（待续）

> 状态：待执行（用户先睡，明天继续）
> 日期：2026-08-04
> 目标：在现有单主题 `Lilac Dream` 基础上，扩展为 5 个紫调主题变体，覆盖从最浅到深色，并打包发布。

## 1. 当前进度

- 图标已更新：用户上传的紫花 logo 已去白底、缩放为 128×128 透明 PNG，替换 `store-assets/icon.png`，commit `e71fd3e` 已 push。
- 已生成 3 张预览对比图（均在 `store-assets/`）：
  - `preview-compare.png`：当前（偏白）vs 优化（淡紫骨架）对照，用于决定是否给基线主题加紫调骨架。
  - `preview-four.png`：4 主题 2×2 网格（Dawn / Dream / Bloom / Dusk）。
  - `preview-five.png`：5 主题竖排网格（Dawn / Dream / Bloom / Dusk / Night）。
- 对应生成脚本：`scripts/generate-preview-compare.py`、`scripts/generate-preview-four.py`、`scripts/generate-preview-five.py`。
- `store-assets/promo/1400x560.png` 与 `440x280.png` 已删除（VS Code 主题扩展不需要 promo 图，按规则不再生成）。

## 2. 五主题调色板（来自预览脚本，已提取为 HEX）

所有颜色为 UI 骨架 + 语法着色统一取色。下面每列为一个主题的核心 token。

| Token | Lilac Dawn 晨薰 | Lilac Dream 梦薰 | Lilac Bloom 盛薰 | Lilac Dusk 暮薰 | Lilac Night 夜薰 |
|-------|----------------|------------------|------------------|-----------------|------------------|
| type | light | light | light | light | **dark** |
| editor.background | #F7F6FA | #F3F1F8 | #EFECF6 | #E4DFEE | #1B162A |
| sideBar.background | #FAF9FD | #F4F1F9 | #ECE7F4 | #E0D9EC | #211B33 |
| activityBar.background | #F5F3F9 | #EDE8F4 | #E3DAEF | #C9BEE0 | #161224 |
| tab.activeBackground | #F7F6FA | #F3F1F8 | #EFECF6 | #E4DFEE | #1B162A |
| tab.inactiveBackground | #F3F1F7 | #E8E2F0 | #DDD2EC | #CEC4DE | #241E38 |
| editorWidget.background | #FDFDFF | #FCFBFD | #F8F5FD | #F0ECF8 | #2A2340 |
| titleBar.activeBackground | #FAF9FD | #F4F1F9 | #ECE7F4 | #E0D9EC | #211B33 |
| statusBar.background | #BE9FE1 | #BE9FE1 | #A67DD8 | #7A4AB8 | #8E5FC8 |
| accent (focus/border) | #BE9FE1 | #BE9FE1 | #A67DD8 | #7A4AB8 | #B38FE6 |
| list.hoverBackground | #DCD0EE | #C9B6E4 | #BE9FE1 | #9A72D0 | #332A4E |
| selection.background | #EFE8F6 | #E1CCEC | #D2B9EA | #B89CDC | #3A2F57 |
| foreground (text) | #332F3C | #2E2A36 | #2A2633 | #231F2D | #E6DFF2 |
| sub/comment | #A699B2 | #9B8CA7 | #8F7EA0 | #7A6A8E | #9B8CB2 |
| keyword | #B38FD9 | #A67DD8 | #8E5FC8 | #6A3CA8 | #C49BEE |
| string | #977AC9 | #8A6BBE | #7857AD | #573A8E | #A67FD8 |

> 注意：4 主题版 Dusk 的 HEX 与 5 主题版不同（4 版 Dusk 偏浅：`#E9E5F1` / `#8E5FC8` accent；5 版 Dusk 更深 `#E4DFEE` / `#7A4AB8` accent）。**最终执行以 `generate-preview-five.py` 的 Dusk 为准**（5 主题方案采用更深的那版），这样 Dawn→Dusk 的浅色梯度更顺、Night 作为唯一深色收尾。

## 3. 各主题定位

- **Lilac Dawn 晨薰**：最浅，近白带极淡紫，适合白天强光环境。
- **Lilac Dream 梦薰（基线）**：当前已发布的主题，淡紫骨架、护眼深紫灰文字。
- **Lilac Bloom 盛薰**：中等饱和度，紫色更明显，适合喜欢紫色但不要太深的用户。
- **Lilac Dusk 暮薰**：最深的浅色主题，黄昏紫，仍是 light uiTheme。
- **Lilac Night 夜薰**：唯一深色主题（uiTheme `vs-dark`），深紫黑底，收尾档。

## 4. 待执行步骤（明天继续）

1. 为每个主题创建独立 theme JSON：
   - `themes/lilac-dawn-color-theme.json`（light）
   - `themes/lilac-dream-color-theme.json`（已有，保持/微调）
   - `themes/lilac-bloom-color-theme.json`（light）
   - `themes/lilac-dusk-color-theme.json`（light）
   - `themes/lilac-night-color-theme.json`（**dark**）
   - 每个 JSON 的 `colors` 与 `tokenColors` 以现有 `lilac-dream-color-theme.json` 为模板，按上表替换对应 HEX，并补齐 terminal/diff/peek 等 token（复用基线色系，按主题明暗调整）。
2. 更新 `package.json` 的 `contributes.themes`，新增 4 个主题的 label / uiTheme / path。
3. 决定是否采用 preview-compare 的「淡紫骨架」优化（把基线 activityBar/titleBar 从纯白 `#FFFFFF` 改为淡紫 `#EDE8F4` / `#F4F1F9`）。建议采用，使整套视觉统一。
4. 生成分语言商店截图 `store-assets/screenshots/{zh,en}/`（按 VS Code 主题规则，不需要 promo）。
5. 更新 README（中英双语，列出 5 个主题 + 预览图）。
6. `vsce package` 打包，并把 `.vsix` 复制到 `D:\迅雷下载\vibe coding\`（无条件默认行为）。
7. 改主题 JSON 后必须重新打包并**重装 vsix**（仅 Reload 不生效）。
8. 提交、推送、弹 BurntToast 通知。

## 5. 关键注意事项

- 深色主题 `Lilac Night` 的 `uiTheme` 为 `vs-dark`，其余 4 个为 `vs`。
- 深色主题的 statusBar/foreground 等需反色（见上表），不要直接复用浅色值。
- 选区/高亮用 8 位 hex 透明度（如 `#E1CCEC80`），浅深主题都通用。
- `package.json` 的 `icon` 已指向 `store-assets/icon.png`，图标无需再改。
- 不需要重建 promo 图（VS Code 主题扩展规则明确不需要）。
- 提交信息用中文一行 ≤ 50 字；不用 `--amend` / `--force`。
