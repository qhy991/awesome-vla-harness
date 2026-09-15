# Observability / Deployment / Model Serving

Harness 的「运行与可见」层：模型服务、环境隔离、轨迹与日志、
以及把评测放进 CI 的部署形态。

目前本仓库尚未收录独立的 observability / model-serving 专用项目，
相关能力主要以上游 Harness 的内建功能形式存在。本页先沉淀**判据**，
条目随贡献逐步补齐（见 [CONTRIBUTING.md](../CONTRIBUTING.md)）。

---

## 现有项目在本层的能力对照

| 项目 | Sandbox / 隔离 | Trajectory / Log 查看 | 部署形态 |
| --- | --- | --- | --- |
| vla-evaluation-harness | Docker 隔离 benchmark | 结果与 episode 记录 | local orchestrator + GPU model server + benchmark 容器 |
| Inspect AI | Docker / Kubernetes / Modal / Proxmox / Vagrant | eval log + Inspect View | local / API / 多种 sandbox |
| lm-evaluation-harness | 非核心抽象 | 结果序列化 | local / 多 GPU / 推理服务器 / API |
| OpenCompass | 非核心抽象 | Summarizer / 榜单 | local / 多 GPU / 推理后端 / API |
| LightEval | 非核心抽象 | sample-level 输出 + EvaluationTracker | local / 多 GPU / endpoint |
| LeRobot | 非核心抽象 | 数据集与录制 | local / 真机 / simulation |
| HELM | 非核心抽象 | Web result viewer | local + API provider |

---

## 部署形态参考

**不要**把模型和 simulator 塞进同一个 container：

```
host / gpu model server
          │
          │ protocol
          ▼
benchmark container
```

构造一个同时携带所有 VLA checkpoint、CUDA、MuJoCo/SAPIEN 与 benchmark assets
的超大镜像，在依赖冲突和镜像体积上都不可持续。

CI 友好的容器示例见 [`docker/Dockerfile.lm-eval`](../docker/Dockerfile.lm-eval)：
CPU、小模型、`--limit` 截断，用来验证升级依赖后 Harness 链路是否仍能运行。

---

## 本层收录判据

一个项目要进入 `observability` / `deployment` / `model-serving` 分类，
至少应提供以下之一：

- [ ] 跨 Harness 可复用的执行隔离机制
- [ ] 轨迹 / transcript 的存储、检索与可视化
- [ ] 评测结果的 provenance 记录（seed / 版本 / 镜像 digest / config hash）
- [ ] 模型推理服务化，且被至少一个 Harness 作为 backend 使用
- [ ] 把评测接入 CI / 定时回归的成熟方案

仅仅是通用 APM、通用日志库或通用容器工具，不在本仓库 scope 内。
