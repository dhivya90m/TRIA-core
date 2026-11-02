"""TRIA core: score a reply, decide, gate. No Streamlit, no UI."""

from .core import (
    LensResult,
    Scorecard,
    decide_release,
    gate_action,
    score_reply,
    STARTING_LENSES,
)

__all__ = [
    "LensResult",
    "Scorecard",
    "decide_release",
    "gate_action",
    "score_reply",
    "STARTING_LENSES",
]
