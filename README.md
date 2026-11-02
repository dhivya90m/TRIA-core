# TRIA core

TRIA is a support agent control plane. It checks a reply before it reaches a customer, then sends it or blocks it.

This repo is the small, readable core of that control plane. No Streamlit, no UI, no network calls, no judge built in.

## What it does

Score one reply across lenses, then decide and gate it:

- `score_reply(customer_request, sop_policy, agent_reply, judge, lenses=None, severity="S2")`
- Returns a scorecard with a release decision, a gate action, failed lenses, and per-lens results.
- A company can add its own lenses. A company-added lens alone can block.

Release decisions: CLEARS THIS SCENARIO, CLEARS WITH REVIEW, HOLD FOR FIX, DO NOT SHIP, SHIP ONLY WITH A TRACKED FIX, INCOMPLETE.

Gate actions: SENT to customer, HELD for human spot-check, BLOCKED and routed to a human, NOT SENT if judging is incomplete.

## What it does not do

TRIA core does not choose your judge, does not run your agent, and does not plug directly into Zendesk, Intercom, or Salesforce. An engineering team imports this core into its own backend, supplies its own judge, and acts on send or block itself. A Zendesk adapter is a separate integration, not this repo.

## Bring your own judge

A judge is a callable:

```python
def judge(customer_request, sop_policy, agent_reply, lens):
    return score, reasoning  # score: float 0.0 to 1.0
```

Your judge can be Gemini, OpenAI, Groq, another model, or a human label wrapped in code. TRIA core does not care which model wrote the reply, or which model judges it. SOP + Policy is the ground truth.

## Example judge, optional

`examples/gemini_judge.py` shows the pattern, using only the Python standard library. It reads the key from `GEMINI_API_KEY` or `GOOGLE_API_KEY` in the environment, never from code. It is an example only, not part of TRIA core, and TRIA core does not import it. If the model call fails, it raises an error, TRIA core marks that lens ERROR, the decision becomes INCOMPLETE, and the gate says NOT SENT.

## Example, no API key needed

```bash
python example.py
```

The example uses a stub judge, so you can read the decision and gate logic in full without any key or network call. Replace the stub with your own judge, and the rest stays the same.

## Tests, no dependencies

```bash
python -m unittest discover -s tests -v
```

## License

This project is licensed under the MIT License. See LICENSE for details.

## Full demo

The full TRIA demo, with a Gemini judge, UI, calibration, batch and transcript import, and a harness gate demo, lives in a separate repo:

https://github.com/dhivya90m/Tria-Support-agent-safety-evaluator

Demo: https://tria-support-agent-safety-evaluator.streamlit.app/
