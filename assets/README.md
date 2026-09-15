# assets/

由 [`scripts/render_charts.py`](../scripts/render_charts.py) 自动生成，**请勿手工编辑**。

| 文件 | 内容 |
| --- | --- |
| `stars-by-project.svg` | 横向柱状图，`log10(stars + 1)` 刻度——仅表示关注度 |
| `maintenance-freshness.svg` | `days_since_last_push` 分桶——表示维护新鲜度 |
| `stats.json` | `update_github_stats.py --json-out` 的带时间戳快照 |

两张图**刻意分开**：项目流行度和维护新鲜度不应被混为一个指标。
log 刻度同样是刻意的，否则量级最大的项目会把新兴 VLA Harness 压到几乎看不见。

在没有运行 `update_github_stats.py` 之前，图中不会有数据——这是预期行为，
因为动态指标从不手工填写。生成顺序：

```bash
GITHUB_TOKEN=... python scripts/update_github_stats.py --json-out assets/stats.json && python scripts/render_charts.py
```
