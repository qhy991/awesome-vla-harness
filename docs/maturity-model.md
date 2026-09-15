# 成熟度模型

## 为什么不用 Stars

Stars 只能作为「关注度」指标，不能单独视为「成熟度」。
2026 年 3 月才创建的 `vla-evaluation-harness` Stars 明显低于 LeRobot，
但从「是否真正解决跨 VLA × benchmark evaluation」这一问题看，
它反而是更直接的 Harness。

本仓库的成熟度综合五个指标：

1. 最近维护时间
2. Release / 版本节奏
3. 测试和可复现机制
4. 集成覆盖面
5. issue / PR 响应情况

Stars 只作为辅助指标。

> **`open_items` 说明**：GitHub API 的 `open_issues_count` 同时包含 issues 和
> pull requests。本仓库把该字段命名为 `open_items`，不要把它误解释为纯 issue 数。

## maturity enum

```
emerging
  新项目；接口、配置或协议仍明显变化。

active
  最近持续提交；有用户和 issue/PR 流；文档可用。

mature
  API 相对稳定；社区较大；长期维护；
  有测试、版本发布和广泛外部使用。

stable
  更新较慢但已有稳定 benchmark / dataset / protocol。

maintenance
  官方明确维护模式，或者只修关键问题。

archived
  官方归档或长期不维护，并已有明确替代。
```

## 当前分布（分析性，非机械式）

```
Mature / Active
├── LeRobot
├── lm-evaluation-harness
├── OpenCompass
└── Inspect AI

Active / Fast-growing
├── vla-evaluation-harness
└── LightEval

Stable / Specialized
├── SimplerEnv
└── LIBERO

Maintenance / Reference
└── Stanford HELM
```

判断依据包括当前维护状态、代码推送时间、社区规模和项目生命周期，
而不仅是 Stars。

## 可视化原则

不要把静态图表永久写进 README——它必然过时。
由每周 Action 生成两张 SVG：

```
assets/stars-by-project.svg
assets/maintenance-freshness.svg
```

**第一张**使用横向柱状图 + `log10(stars + 1)`，
否则量级最大的项目会把新兴 VLA Harness 压到几乎看不见。

**第二张**不要再画 Stars，而画 `days_since_last_push`，并按：

```
0–30 days
31–90 days
91–365 days
>365 days
maintenance / archived
```

分组。这样「项目流行度」和「维护新鲜度」不会被混为一个指标。

## 动态数据纪律

永远标明采样时间：

```json
{
  "project": "lerobot",
  "stats": { "stars": 27476, "fetched_at": "2026-09-14T00:00:00Z" }
}
```

而不是在 README 中写死 `27.5k stars` 然后永远不改。
这能避免 Awesome List 最常见的失败模式：两年后所有元数据都过时。

## 三层更新机制

```
每周
  自动检查链接
  自动刷新 GitHub stars/forks/last_push/open_items
  检查 last_verified 是否超期

每月
  Maintainer review 新项目
  处理 stale entries
  发布 metadata snapshot

每季度
  人工重新评估成熟度
  更新 taxonomy
  增加/移除核心推荐
  发布 curated release notes
```

## 版本发布

curated knowledge repository 更适合 CalVer：

```
v2026.09
v2026.10
v2026.12
v2027.03
```

Release Notes 固定小节：

```markdown
## Added
## Updated
## Deprecated
## Removed
## Taxonomy Changes
## Schema Changes
## Reproducibility Notes
```

只有当 `projects.yaml` / `schema.json` 成为被外部程序消费的稳定 API 时，
再给 schema 自身引入独立 SemVer：

```
repository release: v2027.03
schema_version: 2.1.0
```

## 过期项目策略

不要因「半年没有 commit」就删除研究 benchmark。
像 LIBERO 这类项目，即便更新频率下降，也仍是研究社区的重要 benchmark。
更合理的是状态迁移：

```
active → stable → stale → maintenance / archived
```

只有满足以下条件之一，才把项目从主列表迁到 `entries/archive.md`：

```
官方仓库 archived
官方网站消失且长期无法恢复
官方明确推荐替代项目
依赖已经无法在合理环境中复现
与仓库 scope 不再相关
```

## 治理

```
Maintainer
  ├── taxonomy / schema ownership
  ├── release
  └── disputed entry decision

Reviewer
  ├── project verification
  ├── links / license
  └── reproducibility review

Contributor
  ├── add/update entry
  ├── examples
  └── Chinese resources
```

配合 `CODEOWNERS`，防止一次普通「新增链接」PR 顺手修改 schema 或 CI：

```
/data/                   @maintainers
/docs/taxonomy.md        @maintainers
/examples/               @maintainers @example-reviewers
/.github/                @maintainers
```
