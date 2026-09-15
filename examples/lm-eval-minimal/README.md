# Example A — lm-evaluation-harness CPU 最小评测

**层级**：`LLM-Eval` · **GPU**：不需要 · **上游**：
<https://github.com/EleutherAI/lm-evaluation-harness>

这个示例的目的**不是**得到有意义的 leaderboard 数字，
而是验证完整链路：

```
Task loading
    ↓
Model adapter
    ↓
Generation / log-likelihood request
    ↓
Metric
    ↓
Result serialization
```

## 运行环境

```
OS: Linux / macOS
Python: 3.11
GPU: 不需要，本示例使用 CPU
RAM: 建议 >= 4 GB
Network: 首次运行需要下载模型
```

## 安装

```bash
python -m venv .venv && source .venv/bin/activate && python -m pip install --upgrade pip && pip install "lm_eval[hf]"
```

## 运行

```bash
lm-eval run --model hf --model_args pretrained=EleutherAI/pythia-70m-deduped --tasks hellaswag --device cpu --batch_size 1 --limit 10 --output_path results/lm_eval
```

> 若所用版本尚未提供 `run` 子命令，去掉 `run` 直接使用
> `lm-eval --model hf ...` 即可；请以上游 `lm-eval --help` 为准。

## 在 CI 中使用

保留少量 sample（`--limit`），用它检查升级依赖后 Harness 是否仍能运行，
而不是比较分数。容器化版本见 [`docker/Dockerfile.lm-eval`](../../docker/Dockerfile.lm-eval)。

## 元数据

```
tested_upstream_version: 请在实际验证后填写
last_verified: 2026-09-14
```
