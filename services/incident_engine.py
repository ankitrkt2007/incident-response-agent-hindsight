from app.services.hindsight_client import recall_memories
from app.services.llm import generate_diagnosis

def build_prompt(incident, memories):
    memory_block = "\n\n".join([f"- {m}" for m in memories]) if memories else "No similar past incidents found."

    return f"""
You are diagnosing a production incident.

Incident details:
- Title: {incident.title}
- Service: {incident.service}
- Severity: {incident.severity}
- Symptoms: {incident.symptoms}
- Logs: {incident.logs or "N/A"}

Relevant past incidents recalled from memory:
{memory_block}

Instructions:
1) Give likely root causes (max 3) with reasoning.
2) Provide a prioritized action plan (first 30 minutes).
3) Include what to check if your first hypothesis is wrong.
4) Keep it concrete, no fluff.
"""

def diagnose_incident(incident):
    query = f"{incident.service} {incident.severity} {incident.symptoms} {incident.logs or ''}"
    memories = recall_memories(query, top_k=3)
    prompt = build_prompt(incident, memories)
    diagnosis = generate_diagnosis(prompt)
    return diagnosis, memories
