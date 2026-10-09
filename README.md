# 自旋前沿｜SpinFront

NMR / EPR Daily Brief  
追踪自旋、谱学与应用进展

NMR/EPR 新闻与技术进展的日报归档。内容包括磁共振方法、应用、仪器软件及相关采购信息，每条附摘要、技术评注、发布日期和来源链接。

[在线阅读与检索](https://plastocyanin.org/spinfront/)

## 查阅归档

- 按日期打开完整日报，或设置日期范围检索历史条目。
- 使用全部／NMR／EPR切换方向；双方向条目在NMR、EPR中均可查到。
- 按应用领域筛选，在高级筛选中选择方法、实验类型、信息类型和仪器部件。
- 输入标题、样品、方法或DOI关键词；结果可切换卡片与列表视图。
- 完整日报提供单文件HTML下载，可离线阅读。

同一类别中选择多个标签，显示任一标签对应的条目；不同类别的条件需同时满足。父标签包含其子标签。

## 内容来源与核验

单期JSON保存摘要、技术评注、原始来源及审阅状态。技术评注区分来源结论与分析意见，未确认的实验参数不作补写。分类审阅通过仅表示标签判定，不等同于来源、日期与科学结论均已核实；历史内容的核验状态以记录为准。

日报仅包含文本，不检索或嵌入图片。引用来源的权利归各自权利人。

## 本地构建

需要Python 3；构建脚本仅使用标准库。检索测试需要Node.js。

```sh
python scripts/build.py --check
python scripts/build.py
node tests/search.test.cjs
python -m http.server 8000 --directory _site
```

访问 http://localhost:8000/。构建结果位于 `_site/`，生成的HTML不单独维护。

## 文件与维护

| 路径 | 用途 |
|---|---|
| `data/YYYY/SpinFront_YYYY-MM-DD.json` | 单期内容源 |
| `taxonomy/taxonomy.json` | 受控标签、定义与层级 |
| `templates/home.html`、`assets/home.*` | 归档首页 |
| `assets/search-core.js` | 检索规则与URL条件 |
| `templates/issue.html`、`assets/style.css` | 网页日报与离线HTML模板 |
| `docs/reviews/YYYY-MM-DD.json` | 检索、去重与审阅记录 |

新增JSON后运行数据检查、构建和检索测试。词表版本需与单期记录的 `taxonomy_version` 一致。日期网址为 `YYYY-MM-DD/`，条目锚点为 `SF-YYYYMMDD-NN`。

详细规则见 [每日任务](docs/DAILY_TASK_PROMPT.md)、[输出规范](docs/DAILY_OUTPUT_RULES.md) 与 [维护约定](docs/MAINTENANCE.md)。

## 发布与通知

GitHub Pages使用GitHub Actions构建并发布。提交main分支后触发发布，也可手动运行发布工作流。资源使用相对路径；本项目不配置指向主站域名的CNAME。

钉钉通知由 `.github/workflows/dingtalk-notify.yml` 处理，仅接受 `workflow_dispatch` 触发，不包含 GitHub Actions 定时 cron。北京时间 07:20 为计划推送时间；实际 Cloudflare Worker 触发配置需单独核对。工作流以北京时间判断当日是否已有成功的通知运行，已有记录则跳过，默认手动运行同样适用；`force_send=true` 仅用于明确要求重复发送的人工测试。工作流设置并发串行，避免同一时刻触发的任务同时通过去重检查。检查当日页面 HTTP 200 后，读取仓库 Secret `SPINFRONT_DINGTALK_WEBHOOKS`，向 JSON 中所有 `enabled: true` 的群机器人发送同一条日报，新增、禁用目标只修改 Secret，不修改代码；通知工作流本身不生成日报。异常时工作流记录失败；若部分群已成功收到消息而后续群失败，重新运行可能导致此前成功的群重复收到消息，应先核查发送记录。

## 版权

© 2026 wuhaifeng@ustc.edu.cn. All rights reserved.

日报原创编写内容版权归作者所有，未经许可不得复制、转载或用于商业用途。本仓库暂未授予代码或内容的开放许可。
