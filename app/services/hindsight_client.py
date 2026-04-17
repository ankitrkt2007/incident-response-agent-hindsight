import os
import requests
from typing import List, Dict

HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL", "").rstrip("/")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "")
HINDSIGHT_NAMESPACE = os.getenv("HINDSIGHT_NAMESPACE", "incident-memory")

def _headers():
    return {
        "Authorization": f"Bearer {HINDSIGHT_API_KEY}",
        "Content-Type": "application/json",
    }

def recall_memories(query: str, top_k: int = 3) -> List[str]:
    """
    NOTE:
    Endpoint payload may vary by Hindsight deployment/version.
    Adjust path/fields if needed after checking your Hindsight docs.
    """
    if not HINDSIGHT_BASE_URL or not HINDSIGHT_API_KEY:
        return []

    url = f"{HINDSIGHT_BASE_URL}/api/memory/recall"
    payload = {
        "namespace": HINDSIGHT_NAMESPACE,
        "query": query,
        "top_k": top_k
    }

    try:
        res = requests.post(url, headers=_headers(), json=payload, timeout=20)
        if res.status_code >= 300:
            return []
        data = res.json()
        items = data.get("items", [])
        return [item.get("text", "") for item in items if item.get("text")]
    except Exception:
        return []

def retain_memory(text: str, metadata: Dict):
    """
    NOTE:
    Endpoint payload may vary by Hindsight deployment/version.
    """
    if not HINDSIGHT_BASE_URL or not HINDSIGHT_API_KEY:
        return

    url = f"{HINDSIGHT_BASE_URL}/api/memory/retain"
    payload = {
        "namespace": HINDSIGHT_NAMESPACE,
        "text": text,
        "metadata": metadata
    }

    try:
        requests.post(url, headers=_headers(), json=payload, timeout=20)
    except Exception:
        pass
