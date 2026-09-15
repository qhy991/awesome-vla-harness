# 中文资料

本页维护 Harness / 评测 / VLA 相关的中文资料链接，
原则是**官方中文优先、社区翻译次之**，以免 README 过长。

## 收录原则

1. 官方维护的中文 README / 文档 / 官网优先；
2. 社区翻译需注明对应上游版本或时间，避免长期失同步；
3. 不收录纯营销、无技术内容或无法追溯来源的二手转述；
4. 每条须标注类型：`官方` / `社区` / `课程` / `论文解读`。

## 官方中文资料

| 项目 | 资源 | 类型 |
| --- | --- | --- |
| OpenCompass | [README_zh-CN.md](https://github.com/open-compass/opencompass/blob/main/README_zh-CN.md) | 官方 |
| OpenCompass | [官网 opencompass.org.cn](https://opencompass.org.cn/) | 官方 |

## 待补充

以下方向的高质量中文资料仍较少，欢迎贡献（见 [CONTRIBUTING.md](../CONTRIBUTING.md)）：

- VLA evaluation harness 的环境隔离与复现实践
- Agent harness 的 sandbox 与 tracing 中文说明
- LeRobot 数据格式与真机部署的中文教程
- LIBERO / SimplerEnv 环境依赖排错记录
- harness evolution 相关论文的中文解读

## 术语表

| 英文 | 本仓库用法 | 说明 |
| --- | --- | --- |
| Harness | Harness（保留原文） | 模型权重之外的执行与评测基础设施 |
| Model Adapter | 模型适配层 | 把具体模型接入 Harness 的稳定协议 |
| Benchmark Adapter | Benchmark 适配层 | episode lifecycle 的最小统一接口 |
| Rollout | Rollout / 轨迹执行 | 一次完整的 episode 执行过程 |
| Episode | Episode | 机器人/Agent 的单次任务执行 |
| Action Chunk | 动作块 | VLA 一次推理输出的多步动作序列 |
| Sandbox | Sandbox / 隔离环境 | 容器或虚拟机级别的执行隔离 |
| Held-out task | 留出任务 | 不参与 harness 搜索/优化的评测任务 |
| Test-time scaling | 推理期扩展 | 以更多推理预算换性能的基线方法 |
| Harness tampering | Harness 篡改 | Agent 修改评分器、约束或测试信息等完整性问题 |
| Provenance | 溯源元数据 | seed / 版本 / 镜像 digest / config hash 等 |
