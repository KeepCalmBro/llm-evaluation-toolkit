"""Deterministic rubric evaluation for structured answers."""
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Criterion:
    name: str
    weight: float
    required: tuple[str, ...]
    veto: bool = False


RUBRIC = (
    Criterion("correctness", 0.45, ("answer", "calculation"), True),
    Criterion("method", 0.25, ("assumptions", "steps")),
    Criterion("uncertainty", 0.15, ("limitations",)),
    Criterion("clarity", 0.15, ("summary",)),
)


def evaluate(response: dict) -> dict:
    rows = []
    vetoed = False
    total = 0.0
    for item in RUBRIC:
        present = [key for key in item.required if response.get(key)]
        coverage = len(present) / len(item.required)
        failed_veto = item.veto and coverage < 1.0
        vetoed = vetoed or failed_veto
        total += coverage * item.weight
        rows.append({"criterion": item.name, "coverage": coverage,
                     "missing": [key for key in item.required if key not in present],
                     "veto": failed_veto})
    return {"score": 0.0 if vetoed else round(total, 3),
            "vetoed": vetoed, "criteria": rows}


if __name__ == "__main__":
    sample = {"answer": "5", "calculation": "10 / 2",
              "assumptions": ["synthetic input"],
              "steps": ["divide"], "limitations": ["not validated"],
              "summary": "The stated calculation gives 5."}
    print(json.dumps(evaluate(sample), indent=2))
