"""A one-sample smoke test for an Inspect AI evaluation.

Run with:

    inspect eval examples/inspect-minimal/arithmetic_eval.py \
        --model hf/Qwen/Qwen2.5-0.5B-Instruct
"""

from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import match
from inspect_ai.solver import generate


@task
def arithmetic() -> Task:
    """A one-sample smoke test for an Inspect evaluation."""
    return Task(
        dataset=[
            Sample(
                input="Only output the number. What is 2 + 2?",
                target="4",
            )
        ],
        solver=generate(),
        scorer=match(),
    )
