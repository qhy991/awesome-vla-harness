# LLM Evaluation Harness

成熟的模型适配、任务编排、metric registry 与 plugin 设计参考。
VLA Harness 在这一层几乎不需要重新发明抽象，只需要替换
「task → observation/episode」「metric → success/safety」。

---

## 🟢 lm-evaluation-harness

- Repo: <https://github.com/EleutherAI/lm-evaluation-harness>
- 维护者: EleutherAI · License: MIT · 成熟度: `mature`

通用 LLM few-shot / zero-shot benchmark evaluation，覆盖大量标准 benchmark 与任务子集。

**组件关系**

```
Task / YAML → Request → Model Adapter → Filter → Metric → Aggregation → Output
```

**模型后端**：HF Transformers、vLLM、SGLang、API backend，以及 PEFT 等本地模型路径。

**扩展点**：通过 `lm_eval.*` Python entry points / `--plugins`
扩展 model、filter、metric、aggregation——这一点很适合作为
本仓库后续「插件式兼容层」的设计参考。

**局限**：更偏静态 NLP / LLM benchmark；Agent/sandbox 与 robotics 不是设计中心；
多模态弱于专用 VLM/VLA 工具。

**适合**：LLM 回归测试、benchmark suite、Harness API 设计参考。

快速上手见 [`examples/lm-eval-minimal/`](../examples/lm-eval-minimal/)。

---

## 🟢 OpenCompass

- Repo: <https://github.com/open-compass/opencompass>
- 中文 README: <https://github.com/open-compass/opencompass/blob/main/README_zh-CN.md>
- 官网: <https://opencompass.org.cn/>
- License: Apache-2.0 · 成熟度: `mature`

综合 LLM / VLM evaluation platform，覆盖大量 benchmark、模型与 leaderboard，
官方维护简体中文 README 与文档。

**组件关系**

```
Config → Model + Dataset → Inferencer → Evaluator → Summarizer / Rank
```

**模型后端**：本地模型、API 模型、LMDeploy、vLLM，以及 OpenAI-compatible / LiteLLM 等路径。

**扩展点**：主要通过 config、model wrapper、dataset、inferencer、evaluator 等模块扩展，
不像 lm-eval 那样把 Python entry-point plugin 作为核心。

**局限**：config 和依赖体系较大；不同 acceleration backend 可能带来环境组合复杂度。

**适合**：中文 / 多语 LLM / VLM 综合评估、榜单和大批量实验。

---

## 🟢 LightEval

- Repo: <https://github.com/huggingface/lighteval>
- Docs: <https://huggingface.co/docs/lighteval>
- 维护者: Hugging Face · License: MIT · 成熟度: `active`

更轻量的 LLM evaluation toolkit，内置大量现成 task，
强调 sample-level result 与多 backend 支持。

**组件关系**

```
Task / Metric → Pipeline → Backend → EvaluationTracker → Result
```

**模型后端**：Inspect backend、Accelerate、Nanotron、vLLM、SGLang、
HF endpoints / TGI、LiteLLM 等。

**局限**：与 Inspect 等新 backend 存在部分功能重叠；
Agent isolation 不是其核心能力。

**适合**：Hugging Face 用户、快速 LLM eval、简洁 CI regression。

---

## 🟠 HELM

- Repo: <https://github.com/stanford-crfm/helm>
- Site: <https://crfm.stanford.edu/helm/>
- 维护者: Stanford CRFM · License: Apache-2.0 · 成熟度: `maintenance`

Holistic、reproducible、transparent 的 foundation-model evaluation，
包含效果、效率、bias、toxicity 等多维 metric。

**组件关系**

```
Scenario / RunSpec → Model Provider → Metric → Summarizer → Web / Leaderboard
```

**定位**：对「透明、整体性、标准化评测」的抽象极具参考价值，
但项目已进入 maintenance mode，**不建议作为新项目的默认执行底座**。

**适合**：设计理念、历史结果、综合 metric 参考。
