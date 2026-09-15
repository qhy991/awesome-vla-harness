# Example B — Inspect AI 本地 Agent/Eval 最小程序

**层级**：`Agent-Harness` · **GPU**：可选 · **上游**：
<https://github.com/UKGovernmentBEIS/inspect_ai> · Docs: <https://inspect.aisi.org.uk/>

Inspect 把 Task 抽象为 **Dataset + Solver + Scorer**。
本示例用一个 sample 验证这条链路能跑通。

## 安装

```bash
python -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install inspect-ai torch transformers
```

## 运行

```bash
inspect eval examples/inspect-minimal/arithmetic_eval.py --model hf/Qwen/Qwen2.5-0.5B-Instruct
```

查看运行轨迹：

```bash
inspect view
```

第一次运行需要下载模型；CPU 可以执行，但 GPU 会明显更快。

## 升级为 agent evaluation

当这个例子扩展成 agent evaluation 时，可以沿用 Inspect 官方支持的 sandbox：

```python
return Task(
    dataset=dataset,
    solver=my_agent,
    scorer=my_scorer,
    sandbox="docker",
)
```

Inspect 官方文档中的 CTF 示例正是把 Agent 的 shell / tool execution
放进 Docker sandbox，并用 eval log / Inspect View 检查完整 transcript。

## 元数据

```
tested_upstream_version: 请在实际验证后填写
last_verified: 2026-09-14
```
