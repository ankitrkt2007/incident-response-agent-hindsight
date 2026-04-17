import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3-32b")

def generate_diagnosis(prompt: str) -> str:
    if not GROQ_API_KEY:
        return "No LLM key configured. Please set GROQ_API_KEY in .env"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a senior SRE helping triage incidents."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=40)
        res.raise_for_status()
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"LLM call failed: {str(e)}"
