# Benchmark / Simulator

任务与仿真环境本身。它们**不是** Harness——不提供跨模型 × 跨 benchmark 的
统一执行抽象——但它们是 VLA Harness 最主要的被集成对象，
其依赖栈与资产版本直接决定复现难度。

---

## 🟡 SimplerEnv

- Repo: <https://github.com/simpler-env/SimplerEnv>
- Paper: <https://arxiv.org/abs/2405.05941>
- License: MIT · 成熟度: `stable`

Real-to-sim robot policy / VLA evaluation：
目标是让现实机器人策略能在仿真里进行有相关性的对比。

**组件关系**

```
Sim Env → RGB/State → Policy → Action → Step → Success + Real/Sim Correlation
```

**评估方法**：Visual Matching、Variant Aggregation、real-vs-sim correlation。

**覆盖**：代表性支持 RT-1、RT-1-X、Octo；环境围绕 Google Robot、WidowX/Bridge 等设置。
基于 SAPIEN / ManiSkill 系列，完整模型评测通常需要 NVIDIA GPU / CUDA。

**局限**：任务 / 机器人覆盖有限；simulation 依赖重；
活跃度低于新一代统一 Harness。

**适合**：VLA real-to-sim validation、Google Robot / WidowX 系 benchmark。

---

## 🟡 LIBERO

- Repo: <https://github.com/Lifelong-Robot-Learning/LIBERO>
- Paper: <https://arxiv.org/abs/2306.03310>
- License: 代码 MIT，数据另有数据许可 · 成熟度: `stable`

终身机器人学习 benchmark：130 个任务与多个 task suite
（Spatial / Object / Goal / LIBERO-100），
已成为很多 VLA 工作常用的 manipulation evaluation target。

**组件关系**

```
Task Suite + Demo → Policy → Env Rollout → Success Metric
```

**接入方式**：原生包含 BC 类 baseline；现代 VLA 通常通过 LeRobot、
OpenVLA 项目或 vla-evaluation-harness 等外部 adapter 接入。

**局限**：不是通用 Harness；基础依赖相对较老，环境隔离对复现尤其重要。

**适合**：VLA manipulation benchmark、lifelong / multitask learning。

---

## 收录 benchmark 时的复现 checklist

- [ ] 任务集合与版本是否可识别？
- [ ] assets 来源与校验方式是否明确？
- [ ] seeded reset 是否确定性可测？
- [ ] termination 语义是否显式写明？
- [ ] success 判定条件是否显式写明？
- [ ] action space 与 normalization 约定是否记录？

这些项看似琐碎，但未记录的终止语义与 normalization 细节
足以显著改变最终 success rate。
