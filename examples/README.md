# Example judges

These files are examples only. They are not part of TRIA core, and TRIA core does not import them.

`gemini_judge.py` shows the pattern an engineer follows in their own backend:

- Read the API key from an environment variable, `GEMINI_API_KEY` or `GOOGLE_API_KEY`.
- Never put a key in code.
- Call the judge model, return a score and a reasoning.
- If the call fails, raise an error. TRIA core then marks that lens ERROR, the decision becomes INCOMPLETE, and the gate says NOT SENT.

An engineer can copy this pattern for OpenAI, Groq, or any other model, with their own key handling.
