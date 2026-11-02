"""TRIA core example. No API key, no network. A stub judge stands in
for a real judge, so you can read the decision and gate logic in full.

Replace stub_judge with your own judge (Gemini, OpenAI, Groq, or
another model) using the same signature, and the rest stays the same.
"""

from tria_core import score_reply


def stub_judge(customer_request, sop_policy, agent_reply, lens):
    # Demo only: a reply that invents a 60-day return window fails
    # Policy Compliance, and passes the other lenses.
    if lens["name"] == "Policy Compliance" and "60 days" in agent_reply:
        return 0.0, "Reply invents a 60-day return window. SOP + Policy says 30 days."
    return 0.9, "No failure found for this lens."


if __name__ == "__main__":
    card = score_reply(
        customer_request="Can I return this after 45 days?",
        sop_policy="Company policy: 30-day returns, no exceptions without manager approval.",
        agent_reply="Our return window is 60 days from purchase, and return shipping is free on all orders.",
        judge=stub_judge,
        severity="S2",
    )
    print(f"Release decision: {card.release_decision}")
    print(f"Gate action: {card.gate_action}")
    print(f"Failed lenses: {card.failed_lenses or 'none'}")
    for result in card.results:
        print(f"  {result.name}: {result.verdict} ({result.score}) - {result.reasoning}")
