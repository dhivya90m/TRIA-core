"""Reference judge implementation. Key: GEMINI_API_KEY or GOOGLE_API_KEY, from the environment only."""


import json
import os
import urllib.request


def _api_key():
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("Set GEMINI_API_KEY or GOOGLE_API_KEY in your environment.")
    return key


def gemini_judge(customer_request, sop_policy, agent_reply, lens):
    prompt = (
        "You are a support operations judge. Score one agent reply.\n"
        f"Lens: {lens['name']}\n"
        f"PASS looks like: {lens['pass_looks_like']}\n"
        f"FAIL looks like: {lens['fail_looks_like']}\n"
        f"Customer request: {customer_request}\n"
        f"SOP + Policy: {sop_policy}\n"
        f"Agent reply: {agent_reply}\n"
        "Reply with JSON only, in this exact form: "
        '{"score": 0.0, "reasoning": "..."} '
        "Score 0.0 to 1.0. 0.70 and above is PASS, below 0.70 is FAIL."
    )
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.0-flash:generateContent?key=" + _api_key()
    )
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
    }).encode("utf-8")
    request = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)
    text = payload["candidates"][0]["content"]["parts"][0]["text"]
    result = json.loads(text[text.index("{"):text.rindex("}") + 1])
    return float(result["score"]), str(result["reasoning"])
