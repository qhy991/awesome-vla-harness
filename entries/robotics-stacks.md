# Robot Learning Runtime & Data Stack

训练、数据、模型、硬件与环境的连接层。
这一层不是纯 evaluation harness，但它定义了 VLA 工程中
dataset 格式、policy 接口与真机 I/O 的事实标准，
因此对 Harness 设计有直接影响。

---

## 🟢 LeRobot

- Repo: <https://github.com/huggingface/lerobot>
- Docs: <https://huggingface.co/docs/lerobot>
- 维护者: Hugging Face · License: Apache-2.0 · 成熟度: `active` / `mature`

机器人学习端到端栈：dataset、policy、训练、evaluation、simulator、
real robot、camera、teleoperator 等；已覆盖多种 VLA policy
（如 Pi0 / Pi0Fast / Pi0.5 系列）以及多种 imitation / RL policy，
并与 Hugging Face Hub 深度集成。

**组件关系**

```
Robot / Dataset → Processor → Policy / VLA → Env / Robot → Record / Eval / Train
```

**扩展点**

支持 out-of-tree 的 robot、camera、teleoperator、policy 等插件式 package discovery。
对本仓库而言，这是「插件不进入主仓库」设计最值得参考的实践之一。

**优点**

- 数据、模型、硬件、simulation、VLA 覆盖完整
- 社区体量大
- 真机接口与数据格式统一

**局限**

- Scope 极大，不是纯 evaluation harness
- 硬件、CUDA、robot driver 带来的组合复杂度高

**适合**：VLA / RL / IL 全栈工程、数据集与 policy 标准化、真实机器人。

快速上手见 [`examples/lerobot-dataset/`](../examples/lerobot-dataset/)。

---

## 本层关注的工程维度

真实机器人 hardware-in-the-loop 是当前统一 VLA evaluation 最薄弱的一环
（主流方案仍以 simulation 为主）。值得持续跟踪和规范的维度：

```
control frequency
camera latency
inference latency
action chunking
emergency stop
collision constraints
network degradation
hardware calibration
robot embodiment metadata
real-world reproducibility protocol
```
