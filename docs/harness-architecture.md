# 典型 Harness 架构与设计原则

本文档描述一个同时兼容 LLM Harness 与 VLA Harness 的参考架构，
并给出六条边界划分原则。关键不在具体 class 名称，而在**边界**。

## 参考架构

```
                          ┌──────────────────────┐
                          │   Plugin Registry    │
                          │  task / model / env  │
                          │  tool / metric /     │
                          │  tracker plugins     │
                          └──────────┬───────────┘
                                     │ discovery
                                     ▼
  数据 / Task / Demo / Trajectory
             │
             ▼
  ┌────────────────────────┐
  │ Data Pipeline /        │
  │ Task Adapter           │
  └───────────┬────────────┘
              ▼
  ┌────────────────────────┐        ┌─────────────────────────────┐
  │ Scheduler /            │───────▶│ Environment / Benchmark     │
  │ Orchestrator           │        │ Sandbox (container)         │
  └───────────┬────────────┘        └──────────────┬──────────────┘
              ▼                                     │
  ┌────────────────────────┐                        ▼
  │ Agent / Rollout Loop   │◀──────────  Tools / Robot / Simulator
  └───────────┬────────────┘
              ▼
  ┌────────────────────────┐        ┌─────────────────────────────┐
  │ Model Adapter /        │───────▶│ Model Backend               │
  │ Model Server           │        │ HF / vLLM / SGLang / API /  │
  └───────────┬────────────┘        │ VLA                         │
              │                     └─────────────────────────────┘
              ▼
  ┌────────────────────────┐
  │ Scorer / Evaluator     │
  └───────────┬────────────┘
              ▼
  ┌────────────────────────┐        ┌─────────────────────────────┐
  │ Result & Trajectory    │───────▶│ Monitoring / Tracing /      │
  │ Store                  │        │ Dashboard                   │
  └────────────────────────┘        └─────────────────────────────┘
```

## 六条边界

### 1. Model Adapter / Model Server boundary

Harness 不应该知道 Pi0、OpenVLA、Qwen、Claude 或本地 vLLM 内部如何实现推理。
它只需要一个稳定协议：

```python
class ModelAdapter(Protocol):
    async def predict(self, request: ModelRequest) -> ModelResponse:
        ...
```

对 VLA，可以进一步标准化：

```python
@dataclass
class VLARequest:
    images: list["Image"]
    proprioception: list[float] | None
    instruction: str
    episode_id: str
    step_id: int


@dataclass
class VLAResponse:
    actions: list[list[float]]
    metadata: dict[str, object]
```

这与「一次模型集成、跨 benchmark 使用」的原则一致。

### 2. Environment / Benchmark boundary

统一最低限度的 episode lifecycle：

```python
class BenchmarkAdapter(Protocol):
    def reset(self, task_id: str, seed: int): ...
    def observation(self): ...
    def step(self, action): ...
    def done(self) -> bool: ...
    def result(self) -> dict: ...
```

但**不要**要求所有 benchmark 共享同一个 Python dependency graph。
接口统一和环境统一是两回事：VLA Harness 的正确策略是
**接口统一、环境隔离**。把 simulator 和 model 放进同一个 Python environment，
会把 CUDA / PyTorch / MuJoCo / SAPIEN / Isaac 的依赖组合变成指数级问题。

### 3. Scheduler boundary

Scheduler 管：

```
任务队列
并发数
episode retry
timeout
GPU/worker assignment
failure recovery
```

它不应该直接负责：

```
模型 token/action batching
模型内部 KV cache
模型 checkpoint loading
```

后者属于 Model Server。「并发跑多少 episode」与「模型一次 batch 多少 observation」
是两个不同的控制面；VLA 模型的 batch inference 收益很高，
因此 episode sharding、request batching 与 GPU scheduler 应当分别设计。

### 4. Evaluator boundary

至少区分四类输出：

```
task-native metrics
    success / reward / collision / completion

system metrics
    latency / throughput / GPU memory / cost

reproducibility metadata
    seed / version / image digest / model revision

safety metrics
    forbidden action / unsafe contact / tool policy violation
```

这样同一个 Harness 才能同时服务研究 benchmark 与 production regression。

### 5. Observability boundary

Agent 与 VLA evaluation 都不应只保存一行 `success=1`。至少应记录：

- 模型版本与 revision
- benchmark 版本
- 环境镜像 digest
- 任务 seed
- episode trajectory
- 原始 observation / action metadata
- termination reason
- latency
- 异常
- 最终 metric

未记录的终止语义、action normalization 等细节足以显著改变最终 success rate，
因此 **config provenance 是 Harness 的一等能力，而不是日志附件**。

### 6. Plugin boundary

推荐 Python entry points，而不是一个巨大的 `registry.py`：

```toml
[project.entry-points."awesome_vla.model"]
my_model = "my_package.model:MyModel"

[project.entry-points."awesome_vla.benchmark"]
my_benchmark = "my_package.benchmark:MyBenchmark"

[project.entry-points."awesome_vla.metric"]
my_metric = "my_package.metrics:MyMetric"
```

反例：

```python
ALL_MODELS = {
    "model_a": ModelA,
    "model_b": ModelB,
    # hundreds more...
}
```

要求每一个 model adapter、robot driver、metric 都 merge 进核心仓库，
会迅速制造维护瓶颈。允许 out-of-tree 扩展是更可持续的选择。

## 结果交换 Schema（提案，非强制）

各 Harness 的结果结构目前高度异构。建议的 interchange schema：

```json
{
  "run_id": "...",
  "model": { "name": "...", "revision": "..." },
  "benchmark": { "name": "...", "version": "..." },
  "environment": { "image_digest": "...", "seed": 42 },
  "episode": { "task_id": "...", "success": true, "steps": 123 },
  "system": { "latency_ms": 42, "gpu": "...", "cost": null },
  "provenance": { "harness_version": "...", "config_hash": "..." }
}
```

它不要求任何项目立即兼容；只维护「如何从各框架映射到这个 schema」的
adapter 文档，就已经有价值。

## Conformance Test（提案）

任何 VLA **model adapter** 都应通过：

```
model server starts
health check passes
observation schema validates
one predict() succeeds
action dimensions validate
timeout behaves correctly
failure is serializable
seed is recorded
result contains provenance
```

任何 **benchmark adapter** 都应通过：

```
reset works
deterministic seeded reset is testable
step works
termination semantics are explicit
success condition is explicit
assets/version identifiable
```

## VLA 容器化建议

不要把模型和 simulator 强行塞进同一个 container：

```
host / gpu model server
          │
          │ protocol (websocket / msgpack / grpc)
          ▼
benchmark container
```

这比构造一个同时携带所有 VLA checkpoint、CUDA、MuJoCo/SAPIEN 与 benchmark assets
的超大镜像更符合当前实践。
