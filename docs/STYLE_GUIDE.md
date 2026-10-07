# SpinFront Style Guide

更新日期：2026-10-07（Asia/Shanghai）

用途：保存 SpinFront 当前正式版式与交互要求。跨站共用品牌、字体和页尾规则以主站仓库 `docs/SITE_STYLE_GUIDE.md` 为总备份；本文件只记录 SpinFront 专属实现。

## 1. 品牌与配色

- 深蓝灰：`#203139`
- 链接 / 强调蓝：`#355c7d`
- 金色：`#b68c37`
- 暖白背景：`#f6f6f3` 附近
- serif：Georgia / Times New Roman，用于 SpinFront 品牌、大标题、日期、编号
- sans-serif：正文、标签、筛选与界面

`SpinFront` 中字母 o 使用金色。所有作为品牌显示的 `plastocyanin.` 中，字母 `o` 与末尾圆点均使用金色；其余字母保持深蓝灰。

所有已有语义链接的品牌与标题：
- 默认深蓝灰。
- hover / active / focus 时主体变蓝，并显示细下划线。
- SpinFront 的金色 o，以及 plastocyanin. 的金色 o / 圆点，在 hover / active / focus 时均保持金色。
- 键盘 focus 必须可见。

## 2. 日报主页 `/spinfront/`

主页采用 `Magazine Front Page + Archive`。

首屏：
- 顶部显示 plastocyanin.，链接 `https://plastocyanin.org/`。
- 不在页头增加 Φ 图标。
- 大号 SpinFront 为日报主页链接，保持金色 o。
- 右侧 Latest Issue 使用深蓝灰日期封面块。
- 下方显示最新一期前四条内容及完整日报入口。

归档：
- `EXPLORE THE ARCHIVE` 下提供搜索、刊期日历、主题和高级筛选。
- 搜索结果采用 editorial rows，不使用独立圆角白卡。
- 结果标题使用衬线字体；编号使用金色 `01 /`。
- 技术评注使用金色左线，默认展开，可手动折叠。
- 左侧 sidebar 跟随页面正常滚动，不使用 sticky，不设独立 max-height 或 scrollbar。
- 日期选中状态使用深蓝灰背景、白字、金色标记。
- 最近一期 / 全部日期为一级操作；起止日期、最近7天、本月收进 DATE RANGE。
- “关于归档与数据”和“完整日报归档”保留在主工作区之后，使用全宽折叠布局。
- 最后一条结果不再绘制重复底部分隔线。

## 3. 完整日报 `/spinfront/YYYY-MM-DD/`

采用已确认的 D 版 editorial magazine。

顶部：
- 左侧只有 plastocyanin.；右侧 Daily archive。
- plastocyanin. 返回主站。
- 大号 SpinFront 返回日报主页。
- 右侧深蓝灰日期封面块。
- 封面显示报告数量、NMR/EPR 数量和时间范围。

正文：
- 金色编号、Georgia 标题、细分隔线。
- 桌面端分类标签在右栏；移动端右栏隐藏后，标签移动到标题下。
- 摘要使用正文 sans-serif。
- 技术评注使用金色左线。
- DOI 完整显示并链接 doi.org。
- 来源和替代来源保留链接。
- 检索范围默认折叠。
- 最后一条正文不再显示重复底部分隔线。
- 页尾前提供 Previous / Next Issue。

## 4. 页尾

日报主页和完整日报使用相同的左右双栏关系。

左栏：
- plastocyanin. → 主站
- SpinFront → 日报主页
- 日报主页第三行：`NMR / EPR Daily Brief`
- 单期日报第三行：`NMR / EPR Daily Brief · YYYY-MM-DD`

右栏：
- `© YYYY wuhaifeng@ustc.edu.cn. All rights reserved.`
- `本报告版权归作者所有，未经许可不得复制、转载或用于商业用途。`

桌面端右栏右对齐；移动端改为上下排列、左对齐。

## 5. 钉钉通知

当前结构：

```text
SpinFront | YYYY-MM-DD
> NMR / EPR Daily Brief
本期收录 N 条 · NMR X / EPR Y
内容预览
1. ...
2. ...
3. ...
阅读完整日报 →
```

- 主标题使用略大的 Markdown 标题级别。
- NMR / EPR Daily Brief 使用引用模块。
- 只加粗收录数量。
- 前三条使用普通有序列表，不分别加链接。
- 仅底部“阅读完整日报”链接到当天页面。

## 6. 当前实现文件

- `scripts/build.py`：日报 HTML、主页 Latest Issue、相邻日报、页尾
- `templates/home.html`：日报主页外壳
- `templates/issue.html`：单期日报外壳
- `assets/home.css`：日报主页、归档、日历、搜索结果与页尾
- `assets/home.js`：筛选、检索结果、技术评注默认展开
- `assets/style.css`：完整日报版式
- `.github/workflows/dingtalk-notify.yml`：钉钉消息格式与防重复逻辑

## 7. 保留约束

- 不恢复旧蓝色渐变卡片日报。
- 不恢复 sidebar 独立滚动。
- 不为 SpinFront 页头添加项目 ICO。
- 不取消来源、DOI、检索说明或技术评注。
- 不把桌面右栏标签与标题下标签同时显示造成重复。
- 不取消完整日报 URL 结构。
- 不把钉钉前三条标题改成单独可点击链接，除非用户重新确认。
