# 自旋前沿｜SpinFront

NMR / EPR Daily Brief · 追踪自旋、谱学与应用进展

NMR/EPR日报归档、结构化数据与受控词表。当前包含2026-08-20至2026-10-05的47期、381条记录。主页提供日期定位、全文检索、六维标签筛选和条目浏览；主站布局未改动。

## 内容维护

`data/YYYY/SpinFront_YYYY-MM-DD.json`为单期内容源；`taxonomy/taxonomy.json`为正式词表1.2.0；`assets/style.css`为共享样式；`scripts/build.py`验证数据并生成静态页面。页面地址为`YYYY-MM-DD/`，条目锚点为`SF-YYYYMMDD-NN`。不在仓库中分别维护生成HTML。

```bash
python scripts/build.py --check
python scripts/build.py
python -m http.server 8000 --directory _site
```

Python仅使用标准库。构建结果在`_site/`。新增一期JSON后运行检查，再提交。词表变更与日报中的taxonomy_version同步。JSON审核字段区分分类判定与来源、日期、重复核查。历史分类通过不代表事实核查完成。

## 发布

仓库Settings → Pages → Build and deployment → Source选择GitHub Actions。随后在Actions运行Build and deploy SpinFront，或提交内容触发发布。所有资源使用相对路径，适配项目路径及后续自定义域名。不要配置指向plastocyanin.org的CNAME，以免影响主站域名。

## 版权

© 2026 wuhaifeng@ustc.edu.cn. All rights reserved.

日报原创编写内容版权归作者所有，未经许可不得复制、转载或用于商业用途。引用来源的权利归各自权利人。本仓库暂未授予代码或内容的开放许可。

## 主页

主页模板位于templates/home.html；assets/home.css和home.js维护界面；search-core.js定义检索、层级筛选和URL状态。构建生成轻量search-index.json，不携带原文备份或审核日志。默认最近一期，每次20条。标签同维度OR、跨维度AND，父级包含子级。URL保存条件并支持前进后退。

运行node tests/search.test.cjs验证检索规则，先运行构建。

谱学方向仅保留NMR和EPR；两者均相关时存储两个ID。实验类型按方向分组，方法按用途分组。迁移说明见`docs/taxonomy-migration-1.2.0.json`及维护约定。

## 日报模板与导出

网页日报和可下载单文件HTML共用`templates/issue.html`及`assets/style.css`。构建自动生成`_site/downloads/SpinFront_YYYY-MM-DD.html`，CSS内嵌，可离线阅读。每日执行说明见`docs/DAILY_TASK_PROMPT.md`，检索与审阅过程存放于`docs/reviews/YYYY-MM-DD.json`。
