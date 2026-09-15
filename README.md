# Awesome VLA Harness

> 面向研究者与工程师的 VLA / LLM / Agent Harness、评测框架、
> 机器人学习栈、Benchmark、Runtime 与相关研究精选清单。
>
> 中文优先；项目名称保留原文。

[![Validate](https://github.com/OWNER/awesome-vla-harness/actions/workflows/validate.yml/badge.svg)](../../actions/workflows/validate.yml)
[![Links](https://github.com/OWNER/awesome-vla-harness/actions/workflows/links.yml/badge.svg)](../../actions/workflows/links.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

English version: [README_EN.md](README_EN.md)

## Scope

本仓库中的 **Harness** 指模型权重之外，用于连接模型、数据、任务、
工具、机器人/仿真环境、调度、评估、监控和结果复现的基础设施。

> Harness 是模型权重之外，负责将模型接入任务、环境、工具、数据与评测过程，
> 并控制执行生命周期的一层基础设施。

主要覆盖：

- VLA Evaluation Harness
- LLM Evaluation Harness
- Agent / Runtime Harness
- Robotics Runtime & Data Stack
- Robot Benchmark / Simulator
- Observability / Deployment
- Harness Evolution & Research

不覆盖：单纯的模型权重发布、与执行/评测基础设施无关的论文列表、
没有可验证技术内容的产品营销页。

## Legend

- 🟢 Active：最近持续维护
- 🟡 Stable：成熟但更新频率较低
- 🟠 Maintenance：维护模式，仅建议作为参考
- 🧪 Emerging：新兴项目，API/协议可能快速变化

类型：

- `VLA-Eval`
- `LLM-Eval`
- `Agent-Harness`
- `Robot-Stack`
- `Benchmark`
- `Runtime`
- `Research`

> **动态数据说明**：Stars、fork、最近提交时间等易变字段不写进本文件，
> 由 `data/projects.yaml` 中的 `github_snapshot` 字段与 GitHub Actions 自动刷新，
> 并始终带有采样时间戳。参见 [Maturity Model](docs/maturity-model.md)。

## Contents

- [Core VLA Harnesses](#core-vla-harnesses)
- [Robotics Stacks](#robotics-stacks)
- [LLM Evaluation Harnesses](#llm-evaluation-harnesses)
- [Agent Harnesses](#agent-harnesses)
- [Benchmarks and Simulators](#benchmarks-and-simulators)
- [Research Frontier](#research-frontier)
- [Quickstarts](#quickstarts)
- [Docs](#docs)
- [Contributing](#contributing)
- [License](#license)

## Core VLA Harnesses

- 🧪 [vla-evaluation-harness](https://github.com/allenai/vla-evaluation-harness)
  — `VLA-Eval` · Apache-2.0 · AllenAI
  — 跨 VLA 模型与机器人仿真 Benchmark 的统一评测 Harness；
  模型服务与 Benchmark 进程解耦，并支持环境隔离和并行 Episode 评测。
  [Paper](https://arxiv.org/abs/2603.13966)

详见 [entries/vla-evaluation.md](entries/vla-evaluation.md)。

## Robotics Stacks

- 🟢 [LeRobot](https://github.com/huggingface/lerobot)
  — `Robot-Stack` · Apache-2.0 · Hugging Face
  — 统一机器人数据集、Policy/VLA、训练、Evaluation、Simulation
  与真实硬件接口，并支持外部插件。
  [Docs](https://huggingface.co/docs/lerobot)

详见 [entries/robotics-stacks.md](entries/robotics-stacks.md)。

## LLM Evaluation Harnesses

- 🟢 [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
  — `LLM-Eval` · MIT · EleutherAI
  — 成熟的 LLM benchmark Harness，支持大量任务、模型后端、
  Metric/Filter/Aggregation 与插件扩展。

- 🟢 [OpenCompass](https://github.com/open-compass/opencompass)
  — `LLM-Eval` · Apache-2.0
  — 面向大规模 LLM/VLM 的综合评测平台，中文文档完善，
  支持本地模型、推理后端和 API 模型。
  [中文 README](https://github.com/open-compass/opencompass/blob/main/README_zh-CN.md)
  · [官网](https://opencompass.org.cn/)

- 🟢 [LightEval](https://github.com/huggingface/lighteval)
  — `LLM-Eval` · MIT · Hugging Face
  — 轻量、多后端的 LLM 评测工具，适合快速实验和 HF 工作流。
  [Docs](https://huggingface.co/docs/lighteval)

- 🟠 [HELM](https://github.com/stanford-crfm/helm)
  — `LLM-Eval` · Apache-2.0 · Stanford CRFM
  — Holistic / Transparent / Reproducible 模型评测的重要参考项目；
  当前处于 maintenance mode。
  [Site](https://crfm.stanford.edu/helm/)

详见 [entries/llm-evaluation.md](entries/llm-evaluation.md)。

## Agent Harnesses

- 🟢 [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai)
  — `Agent-Harness` · MIT · UK AI Security Institute / Meridian Labs
  — 支持 Task、Agent、Tool、Sandbox、Scorer、Tracing、
  Multi-Agent 和可扩展 Model Provider。
  [Docs](https://inspect.aisi.org.uk/)

详见 [entries/agent-runtime.md](entries/agent-runtime.md)。

## Benchmarks and Simulators

- 🟡 [SimplerEnv](https://github.com/simpler-env/SimplerEnv)
  — `Benchmark` · MIT
  — 面向真实机器人 Policy/VLA 的 real-to-sim evaluation framework。
  [Paper](https://arxiv.org/abs/2405.05941)

- 🟡 [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO)
  — `Benchmark` · MIT（代码）
  — 经典 lifelong robot learning / manipulation benchmark，
  包含多套任务集合并广泛用于 VLA evaluation。
  [Paper](https://arxiv.org/abs/2306.03310)

详见 [entries/benchmarks-simulators.md](entries/benchmarks-simulators.md)。

## Research Frontier

- [Life-Harness](https://arxiv.org/abs/2605.22166)
  — Runtime harness adaptation for frozen LLM agents.

- [Rethinking the Evaluation of Harness Evolution for Agents](https://arxiv.org/abs/2607.12227)
  — Harness evolution 的预算公平性、过拟合与 held-out evaluation。

- [HarnessDev](https://arxiv.org/abs/2609.01437)
  — 将可运行 Harness 的创建和演化本身作为 Benchmark。

- [HarnessCompass](https://arxiv.org/abs/2608.01918)
  — 约束式、component-wise automatic harness evolution。

详见 [entries/research-frontier.md](entries/research-frontier.md)。

## Quickstarts

四个示例分别覆盖 Harness 的不同层级，而不是同一框架的教程集合：

| 示例 | 层级 | GPU | 说明 |
| --- | --- | --- | --- |
| [`examples/lm-eval-minimal/`](examples/lm-eval-minimal/) | LLM-Eval | 否 | CPU 上的最小 benchmark 链路 smoke test |
| [`examples/inspect-minimal/`](examples/inspect-minimal/) | Agent-Harness | 可选 | Task = Dataset + Solver + Scorer 的最小程序 |
| [`examples/lerobot-dataset/`](examples/lerobot-dataset/) | Robot-Stack | 否 | 不接机器人的数据层 smoke test |
| [`examples/vla-eval-smoke/`](examples/vla-eval-smoke/) | VLA-Eval | 是 | Model Server 与 Benchmark Runner 分离的 VLA 评测 |

容器示例见 [`docker/Dockerfile.lm-eval`](docker/Dockerfile.lm-eval)。

## Docs

- [分类体系 Taxonomy](docs/taxonomy.md)
- [典型 Harness 架构与设计原则](docs/harness-architecture.md)
- [成熟度模型](docs/maturity-model.md)
- [中文资料](docs/chinese-resources.md)

## Contributing

新增项目请同时：

1. 修改 `data/projects.yaml`
2. 修改对应 `entries/*.md`
3. 提供官方仓库、许可、官方文档或原始论文
4. 完成 `last_verified`
5. 通过 schema 和链接检查

详细规则见 [CONTRIBUTING.md](CONTRIBUTING.md)。

本地检查：

```bash
python scripts/validate_entries.py && python scripts/check_links.py
```

## License

本仓库自身内容和示例代码采用 Apache-2.0（见 [LICENSE](LICENSE)）。

被索引项目、模型、数据集、Benchmark 和论文继续受各自许可证约束；
本仓库中的收录不改变任何上游许可条件，详见 [NOTICE](NOTICE)。
