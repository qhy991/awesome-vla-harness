# Docker 示例

## `Dockerfile.lm-eval`

CPU-only 的 lm-evaluation-harness smoke image，用于 CI 验证 Harness 链路。

构建：

```bash
docker build -t awesome-vla-harness:lm-eval -f docker/Dockerfile.lm-eval .
```

执行：

```bash
docker run --rm -v "$PWD/results:/workspace/results" -v awesome-vla-hf-cache:/cache/huggingface awesome-vla-harness:lm-eval
```

## 为什么没有「一个 VLA 大镜像」

后续 VLA Docker 示例不建议把模型和 simulator 塞进同一个 container。
更合理的是：

```
host / gpu model server
          │
          │ protocol
          ▼
benchmark container
```

传统 per-model / per-benchmark 环境会产生大量依赖冲突，
这正是解耦方案存在的原因。详见
[docs/harness-architecture.md](../docs/harness-architecture.md)。
