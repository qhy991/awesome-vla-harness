# Contributing

感谢你帮助维护 Awesome VLA Harness。

本仓库强调：

- 一手来源
- 可验证性
- 中立描述
- 明确 License
- 可复现信息
- 对项目活跃度的时间戳记录

## 可接受的项目

原则上至少满足：

1. 与 VLA / LLM / Agent Harness、评测、Runtime、
   Robot Benchmark 或 Harness Research 直接相关；
2. 有公开且稳定的官方项目页、代码仓库或论文；
3. License 可以明确识别；
4. 能给出至少一个实际使用方式；
5. 不只是营销页面或没有可验证技术内容的产品介绍。

新兴研究项目可进入 `Research Frontier`，
不要求和成熟工程项目达到同等稳定度。

## 新增项目

请：

1. 在 `data/projects.yaml` 中添加项目；
2. 在对应 `entries/*.md` 中添加短描述；
3. 使用官方仓库、官方文档、项目主页或原始论文作为来源；
4. 标明代码和数据 License；
5. 填写 `last_verified: YYYY-MM-DD`；
6. **不要手工填写 Stars 等动态指标**（`github_snapshot` 由 CI 注入）。

项目描述应尽量控制在两句话内，不使用：

- “最佳”
- “最强”
- “SOTA”

除非有明确的 benchmark 和一手证据。

### 条目最小字段

`data/projects.yaml` 中每个条目必须包含：

```
id
name
organization
url
category[]
license
capabilities
backends[]
deployment[]
evaluation[]
maturity
last_verified
references[]
```

可选字段：`docs`、`paper`、`description_zh`、`notes`、`github_snapshot`。

## 本地检查

```bash
python -m pip install pyyaml
python scripts/validate_entries.py
python scripts/check_links.py
```

`check_links.py` 会做网络请求，建议在 PR 前至少跑一次
`python scripts/check_links.py --changed-only`。

## PR 命名

推荐：

```
add: <project-name>
update: <project-name>
fix: broken links for <project-name>
docs: improve <topic>
chore: refresh metadata
```

## License 注意事项

本仓库 License 仅覆盖本仓库原创内容。

上游项目、模型权重、数据集、机器人资产和论文继续受各自 License / Terms 约束。

请避免直接复制大段上游代码或文档；优先链接官方来源并自行概述。

以上为工程治理建议，不构成法律意见；特定模型、数据集或商业部署场景请自行进行法律审查。

## 审核标准

Maintainer 会检查：

- 是否重复
- 分类是否正确
- 官方来源是否存在
- License 是否准确
- 项目是否实际与 Harness 有关
- 描述是否中立
- 活跃度标签是否合理
- 链接检查是否通过

## Harness Evolution 类工作的额外 checklist

若提交的是自动 harness evolution / self-improving harness 相关研究，请在 PR 中说明：

- 是否使用 held-out evaluation？
- 搜索集和测试集是否分离？
- 是否报告 Harness evolution token budget？
- 是否与相同 inference budget 的 test-time scaling 比较？
- 是否在不同模型上测试 transfer？
- 是否记录 Harness modification history？
