# VLA Evaluation Harness

跨 VLA 模型、跨机器人 benchmark 的执行与评测框架。
这一层的定义性问题不是「模型怎么调用」，而是
**如何让同一个模型在依赖互不兼容的多个 benchmark 上被公平、可复现地评测**。

---

## 🧪 vla-evaluation-harness

- Repo: <https://github.com/allenai/vla-evaluation-harness>
- Docs: <https://allenai.github.io/vla-evaluation-harness/>
- Paper: <https://arxiv.org/abs/2603.13966>
- 维护者: AllenAI · License: Apache-2.0 · 成熟度: `emerging`

专门解决跨 VLA、跨机器人仿真 benchmark 的评估问题：
模型一次接入、benchmark 一次接入，再自动形成 cross-product evaluation 矩阵。

**组件关系**

```
Orchestrator
   → Benchmark / Episode Runner
        ↕ WebSocket + msgpack
      Model Server
   → Result / Tracker
```

benchmark 依赖以容器隔离，模型推理进程与 benchmark 进程分离。

**扩展点**

- Model server 实现统一 `predict()`
- Benchmark 通过精简 adapter interface 接入
- 配置文件描述模型 × benchmark 的组合

**为什么重要**

在此之前，VLA 通常依赖各模型仓库维护各自的 benchmark 脚本，
由此产生代码重复、dependency conflict 和 underspecified evaluation protocol。
其 LIBERO 批量评估实验报告了最高约 47× 的吞吐提升
（2000 episodes 从约 14h 降到约 18min）。

**局限**

- 项目年轻，模型/benchmark protocol 仍可能快速迭代
- simulation-first，真机 hardware-in-the-loop 覆盖有限
- GPU、镜像和资产成本不小

**适合**：VLA leaderboard、跨 benchmark reproduction、模型回归测试。

快速上手见 [`examples/vla-eval-smoke/`](../examples/vla-eval-smoke/)。

---

## 相关但不属于本层

- **LeRobot** 含 VLA policy 与 evaluation 能力，但 scope 是完整机器人学习栈，
  见 [robotics-stacks.md](robotics-stacks.md)。
- **SimplerEnv / LIBERO** 是 benchmark-specific evaluation environment，
  而非跨 benchmark harness，见 [benchmarks-simulators.md](benchmarks-simulators.md)。

## 本层的评估 checklist

收录新的 VLA harness 时，建议核对：

- [ ] 模型接入是否只需实现一个稳定接口？
- [ ] benchmark 依赖是否被隔离（容器 / 独立环境）？
- [ ] 是否记录 seed、镜像 digest、模型 revision、config hash？
- [ ] termination 语义与 action normalization 是否显式记录？
- [ ] episode sharding 与 model batching 是否分离设计？
- [ ] 失败 episode 是否可序列化并可复现？
