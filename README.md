# LLM Evaluation Toolkit

A small rules-based evaluator for structured model answers. It uses a weighted rubric and returns a JSON record of the score, missing evidence, and any hard failure.

## Design

- Each criterion has a weight and required fields.
- Missing evidence is reported by name.
- A correctness failure can set the final score to zero.
- The output is deterministic and easy to inspect.

## Run

```bash
python3 evaluator.py
```

The example is synthetic. It contains no vendor prompts, tasks, or model output.
