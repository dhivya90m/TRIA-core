# Example judges

Reference implementations only. TRIA core does not import them.

`gemini_judge.py` reads the key from `GEMINI_API_KEY` or `GOOGLE_API_KEY` in the environment. On failure, it raises an error. TRIA core marks that lens ERROR, the decision becomes INCOMPLETE, and the gate says NOT SENT.
