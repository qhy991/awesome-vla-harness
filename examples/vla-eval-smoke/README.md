# Example D — vla-eval VLA smoke test

**层级**：`VLA-Eval` · **GPU**：需要 · **上游**：
<https://github.com/allenai/vla-evaluation-harness>

这是本仓库最应该重点展示的示例，因为它真正体现
**Model Server 与 Benchmark Runner 分离**：核心调用模式就是
`serve` + `run` 两个独立进程。

## 推荐环境

```
Linux
Python 3.11
uv
Docker
NVIDIA GPU + 对应驱动
足够的模型 checkpoint / Docker image 存储
```

## 安装（固定 tag，保证 config 与版本一致）

```bash
git clone --branch v0.5.0 https://github.com/allenai/vla-evaluation-harness.git
```

```bash
cd vla-evaluation-harness && uv sync --python 3.11 --all-extras --dev
```

## 运行

终端 A —— 启动模型服务：

```bash
uv run vla-eval serve -c configs/model_servers/db_cogact/libero.yaml
```

终端 B —— 运行 LIBERO smoke evaluation：

```bash
uv run vla-eval run -c configs/benchmarks/libero/smoke_test.yaml
```

## 为什么固定版本

具体 config 名会随项目版本演进，因此本仓库**不复制大量上游 config**，
而是固定某个已验证 tag。VLA 的 benchmark protocol、assets、
checkpoint normalization 和环境版本都可能改变，
未记录的参数甚至可能显著改变最终 success rate。

## 元数据

```
tested_upstream_version: v0.5.0
last_verified: 2026-09-14
```

> 请在本地实际验证后更新上述两行；若上游 tag 或 config 路径已变化，
> 请提交 `fix:` PR 并同步 `data/projects.yaml` 的 `last_verified`。
