# 自旋前沿｜SpinFront

NMR / EPR Daily Brief · 追踪自旋、谱学与应用进展

NMR/EPR日报归档、结构化数据与受控词表。当前包含2026-08-20至2026-10-05的47期、381条记录。主页暂保留日期归档，后续设计日历及多级检索。

## 内容维护

`data/YYYY/SpinFront_YYYY-MM-DD.json`为单期内容源；`taxonomy/taxonomy.json`为正式词表1.0.0；`assets/style.css`为共享样式；`scripts/build.py`验证数据并生成静态页面。页面地址为`YYYY-MM-DD/`，条目锚点为`SF-YYYYMMDD-NN`。不在仓库中分别维护生成HTML。

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
