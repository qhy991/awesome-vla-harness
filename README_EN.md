# Awesome VLA Harness

> A curated, evidence-based list of VLA / LLM / Agent harnesses, evaluation
> frameworks, robot benchmarks, runtimes, and harness research.
>
> The primary language of this repository is Chinese; see [README.md](README.md).

## Scope

A **harness**, as used here, is the infrastructure *outside the model weights*
that connects a model to tasks, environments, tools and data, and that controls
the execution lifecycle — scheduling, sandboxing, scoring, logging and
reproducibility.

Covered layers:

- VLA Evaluation Harness
- LLM Evaluation Harness
- Agent / Runtime Harness
- Robotics Runtime & Data Stack
- Robot Benchmark / Simulator
- Observability / Deployment
- Harness Evolution & Research

## Legend

- 🟢 Active · 🟡 Stable · 🟠 Maintenance · 🧪 Emerging

Types: `VLA-Eval`, `LLM-Eval`, `Agent-Harness`, `Robot-Stack`, `Benchmark`,
`Runtime`, `Research`.

Volatile metrics (stars, forks, last push) are **not** written into the
Markdown. They live in `data/projects.yaml` under `github_snapshot` and are
refreshed by GitHub Actions with an explicit `fetched_at` timestamp.

## Core VLA Harnesses

- 🧪 [vla-evaluation-harness](https://github.com/allenai/vla-evaluation-harness)
  — `VLA-Eval` · Apache-2.0 · AllenAI — unified evaluation across VLA models and
  robot simulation benchmarks; model server and benchmark processes are
  decoupled, benchmarks run in isolated containers, episodes run in parallel.

## Robotics Stacks

- 🟢 [LeRobot](https://github.com/huggingface/lerobot) — `Robot-Stack` ·
  Apache-2.0 · Hugging Face — datasets, policies/VLAs, training, evaluation,
  simulation and real hardware behind one set of interfaces, with out-of-tree
  plugins.

## LLM Evaluation Harnesses

- 🟢 [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) — `LLM-Eval` · MIT · EleutherAI
- 🟢 [OpenCompass](https://github.com/open-compass/opencompass) — `LLM-Eval` · Apache-2.0
- 🟢 [LightEval](https://github.com/huggingface/lighteval) — `LLM-Eval` · MIT · Hugging Face
- 🟠 [HELM](https://github.com/stanford-crfm/helm) — `LLM-Eval` · Apache-2.0 · Stanford CRFM (maintenance mode)

## Agent Harnesses

- 🟢 [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) —
  `Agent-Harness` · MIT · UK AI Security Institute / Meridian Labs

## Benchmarks and Simulators

- 🟡 [SimplerEnv](https://github.com/simpler-env/SimplerEnv) — `Benchmark` · MIT
- 🟡 [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO) — `Benchmark` · MIT (code)

## Research Frontier

- [Life-Harness](https://arxiv.org/abs/2605.22166) — runtime harness adaptation for frozen LLM agents
- [Rethinking the Evaluation of Harness Evolution for Agents](https://arxiv.org/abs/2607.12227)
- [HarnessDev](https://arxiv.org/abs/2609.01437)
- [HarnessCompass](https://arxiv.org/abs/2608.01918)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Every change must update both
`data/projects.yaml` (the source of truth) and the matching `entries/*.md`
(the human-readable layer), and must pass:

```bash
python scripts/validate_entries.py && python scripts/check_links.py
```

## License

Apache-2.0 for this repository's own content. Indexed projects, models,
datasets, benchmarks and papers remain under their own licenses; see
[NOTICE](NOTICE).
