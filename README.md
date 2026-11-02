# TRIA core

TRIA is a support agent control plane. It checks a reply before it reaches a customer, then sends it or blocks it.

TRIA core contains the score, decision, and gate logic for that control plane.

## Usage

```python
from tria_core import score_reply

card = score_reply(
    customer_request=request,
    sop_policy=sop_policy,
    agent_reply=agent_reply,
    judge=judge,
    severity="S2",
)
```

Returns a scorecard with a release decision, a gate action, failed lenses, and per-lens results.

A company can add its own lenses. A company-added lens alone can block.

## Judge interface

```python
def judge(customer_request, sop_policy, agent_reply, lens):
    return score, reasoning  # score: float 0.0 to 1.0
```

SOP + Policy is the ground truth. TRIA core does not select the judge model.

## Release decisions

CLEARS THIS SCENARIO, CLEARS WITH REVIEW, HOLD FOR FIX, DO NOT SHIP, SHIP ONLY WITH A TRACKED FIX, INCOMPLETE.

## Gate actions

SENT to customer, HELD for human spot-check, BLOCKED and routed to a human, NOT SENT if judging is incomplete.

## Example

```bash
python example.py
```

The example uses a stub judge and requires no API key. `examples/gemini_judge.py` provides a reference judge implementation. The key is read from `GEMINI_API_KEY` or `GOOGLE_API_KEY` in the environment.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT License. See LICENSE for details.

## Full demo

https://github.com/dhivya90m/Tria-Support-agent-safety-evaluator

Demo: https://tria-support-agent-safety-evaluator.streamlit.app/
