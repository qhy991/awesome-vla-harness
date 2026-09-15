# 分类体系 Taxonomy

本仓库采用**五层分类**，而不是把框架、benchmark 和论文平铺在一个列表里。

```
1. VLA Evaluation Harness      跨模型、跨 benchmark 的执行与评测框架
2. LLM / Agent Harness         模型适配、任务编排、sandbox、logging、plugin 设计参考
3. Robot Learning Runtime      训练、数据、模型、硬件与环境连接层
4. Benchmark / Simulator       任务与仿真环境
5. Harness Research Frontier   runtime harness、automatic evolution、held-out 评测、安全与完整性
```

## category enum

`data/projects.yaml` 中的 `category` 必须取自以下固定集合
（同一项目可以属于多个 category）：

```yaml
categories:
  - vla-evaluation
  - llm-evaluation
  - agent-runtime
  - robotics-stack
  - benchmark
  - simulator
  - model-serving
  - observability
  - deployment
  - safety-evaluation
  - harness-evolution
  - research
```

`entries/*.md` 与 category 的对应关系：

| 文件 | 覆盖 category |
| --- | --- |
| `entries/vla-evaluation.md` | `vla-evaluation` |
| `entries/llm-evaluation.md` | `llm-evaluation` |
| `entries/agent-runtime.md` | `agent-runtime`、`safety-evaluation` |
| `entries/robotics-stacks.md` | `robotics-stack` |
| `entries/benchmarks-simulators.md` | `benchmark`、`simulator` |
| `entries/observability-deployment.md` | `observability`、`deployment`、`model-serving` |
| `entries/research-frontier.md` | `research`、`harness-evolution` |

## GitHub Labels

标签按**正交维度**组织，避免几十个彼此重叠的自由标签。

| 维度 | 标签 |
| --- | --- |
| 变更类型 | `type:add-project`、`type:update`、`type:docs`、`type:broken-link`、`type:automation` |
| 技术领域 | `area:vla`、`area:llm`、`area:agent`、`area:benchmark`、`area:runtime`、`area:data`、`area:observability`、`area:deployment`、`area:safety` |
| 成熟度 | `maturity:emerging`、`maturity:active`、`maturity:mature`、`maturity:maintenance`、`maturity:archived` |
| 后端 | `backend:hf`、`backend:vllm`、`backend:sglang`、`backend:api`、`backend:simulator`、`backend:real-robot` |
| 证据 | `evidence:paper`、`evidence:official-docs`、`evidence:reproduced` |
| 工作流 | `status:needs-triage`、`good-first-issue`、`help-wanted`、`blocked` |

## Harness 的三种形态

**Evaluation Harness**

```
Dataset / Task → Model Adapter → Inference → Post-process → Metric → Aggregation → Report
```

**Agent / Runtime Harness**

```
Observation → Prompt/Memory → Model → Tool/Action → Environment → Feedback → Controller → 下一轮
```

**VLA Execution Harness**

```
Camera/State → Observation Adapter → VLA → Action Chunk → Robot/Simulator → Episode State → Success/Safety Metric
```

三者共享同样的边界划分原则，差别在于 VLA 多出一层机器人环境特有的
依赖与资产约束：每个 benchmark 往往带有完全不同的 CUDA、MuJoCo/SAPIEN/Isaac、
Python 版本与 asset 依赖。详见 [harness-architecture.md](harness-architecture.md)。
