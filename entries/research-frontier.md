# Harness Research Frontier

2026 年，Harness 不再只是 evaluation runner，而本身成为**被优化和被评测的对象**。
本页收录 runtime harness、automatic harness evolution、held-out harness evaluation
以及 harness 安全与完整性相关工作。

收录标准比工程项目宽松（`maturity: emerging` 可接受），
但必须给出原始论文链接。

---

## runtime-harness

### Life-Harness

- Paper: <https://arxiv.org/abs/2605.22166>

Runtime harness adaptation for frozen LLM agents。
不改模型，而改「模型与环境之间的 interface/harness」本身：
从训练轨迹中总结 environment contract、procedural skill、
action realization 与 trajectory regulation 相关干预，
并在 held-out evaluation 时**冻结** Harness。

**价值**：论证了 prompts、tools、memory、control flow、action realization 等
模型外部系统可以作为独立的优化对象。

---

## harness-evaluation

### Rethinking the Evaluation of Harness Evolution for Agents

- Paper: <https://arxiv.org/abs/2607.12227>

对 harness evolution 的预算公平性与同 benchmark 过拟合问题提出系统质疑。

**核心警告**：如果 Harness 使用 public test cases 反复演化，
再在同一 test set 报最终成绩，那么提升可能来自额外搜索预算或直接过拟合。
在匹配 feedback / inference budget 并加入 held-out task 后，
自动 harness evolution 并不总能超过简单的 test-time scaling，
而且 generalization 可能有限。

**由此产生的评测规范**：held-out task、固定计算预算、完整运行轨迹。

---

## harness-generation

### HarnessDev

- Paper: <https://arxiv.org/abs/2609.01437>

把「创建、演化可执行 Harness」本身作为 benchmark，
将评测单位从最终答案提升到**可运行基础设施**。

---

## harness-evolution

### HarnessCompass

- Paper: <https://arxiv.org/abs/2608.01918>

探索约束式、component-wise 的 automatic harness evolution，
并强调向 held-out task / 不同模型的 transfer。

---

## Harness Evolution 评测 checklist

提交此类工作时，请在 PR 中回答：

- [ ] 是否使用 held-out evaluation？
- [ ] 搜索集和测试集是否分离？
- [ ] 是否报告 Harness evolution token budget？
- [ ] 是否与相同 inference budget 的 test-time scaling 比较？
- [ ] 是否在不同模型上测试 transfer？
- [ ] 是否记录 Harness modification history？

---

## 待跟踪方向：Harness Integrity / Tampering

随着 agent 可以编辑自己的 prompts、tools、policy 和 evaluator，
必须区分**真正的能力提升**与：

```
修改评分器
修改权限约束
泄漏测试信息
隐藏失败轨迹
扩大未经报告的 compute budget
```

这一问题已被称为 *harness tampering*，很可能成为 Harness 工程
与安全评测的新子领域。相关工作欢迎提交到本页。
