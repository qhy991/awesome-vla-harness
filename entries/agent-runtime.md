# Agent / Runtime Harness

这一层的核心差异在于执行不再是「一次前向推理」，而是
**Observation → Prompt/Memory → Model → Tool/Action → Environment → Feedback → 下一轮**
的闭环。因此 sandbox、tracing、轨迹存储与多智能体协作成为一等能力。

---

## 🟢 Inspect AI

- Repo: <https://github.com/UKGovernmentBEIS/inspect_ai>
- Docs: <https://inspect.aisi.org.uk/>
- 维护者: UK AI Security Institute / Meridian Labs · License: MIT · 成熟度: `mature`

从 benchmark 到 agent / autonomy / security evaluation，
尤其适合 tool-use、代码执行与长轨迹 Agent。

**组件关系**

```
Task = Dataset + Solver/Agent + Scorer
Agent ↔ Tools ↔ Sandbox
全过程 → eval log / Inspect View
```

**能力**

- 自定义工具与 MCP 工具
- Docker / Kubernetes / Modal / Proxmox / Vagrant 等 sandbox
- 外部 agent（Claude Code、Codex CLI、Gemini CLI 等）
- multi-agent、checkpointing、tracing
- 网页版 Log Viewer / Inspect View
- 多种 model provider，以及 HF / vLLM / SGLang 本地推理

**扩展点**：Model APIs、components、sandboxes、approvers、hooks、filesystems，
支持以 Python package 形式扩展。

**局限**：API / 概念比「跑几个 benchmark」的工具更重；robotics / VLA 不是原生重点。

**适合**：Agent、coding、tool-use、安全 / 自治能力评测。

快速上手见 [`examples/inspect-minimal/`](../examples/inspect-minimal/)。

---

## 对 VLA 的启示

Agent 评估不只保存一个 score，而是可以查看完整执行 transcript，
并针对工具与 sandbox 行为做分析。VLA Harness 也应把每个 episode 的
`observation → action → environment feedback` 视为 trajectory，
而非只有一行 `success=1`。

安全相关维度（`safety-evaluation`）同样适用于 VLA：

```
forbidden action
unsafe contact / collision
tool policy violation
constraint bypass
```
