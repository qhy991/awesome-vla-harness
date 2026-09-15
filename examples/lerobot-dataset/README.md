# Example C — LeRobot 无机器人数据层 smoke test

**层级**：`Robot-Stack` · **GPU**：不需要 · **上游**：
<https://github.com/huggingface/lerobot> · Docs: <https://huggingface.co/docs/lerobot>

一个「不接机器人也能跑」的 dataset smoke test，
比直接要求购买硬件更适合作为最初示例。它验证：

```
Hub Dataset
    ↓
LeRobotDataset
    ↓
Standard observation / action representation
    ↓
Policy / Train / Evaluation
```

## 安装

```bash
python -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install lerobot
```

## 运行

```bash
python examples/lerobot-dataset/inspect_dataset.py
```

首次运行会从 Hugging Face Hub 拉取数据，因此不像纯文本 benchmark 那么轻。

## 后续

可在 `examples/lerobot-eval/` 增加真正的 Pi0 / SmolVLA + LIBERO 示例，
并把 GPU 依赖与 benchmark environment 单独写清楚。

## 元数据

```
tested_upstream_version: 请在实际验证后填写
last_verified: 2026-09-14
```
