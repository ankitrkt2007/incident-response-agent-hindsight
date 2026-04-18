# Building an Incident Response Agent with Hindsight Memory (FastAPI + Groq)

Production incidents are chaotic by nature. The same kinds of failures happen repeatedly—database pool exhaustion, misconfigured timeouts, sudden traffic spikes—yet teams often start triage from scratch every time.

I built a lightweight **Incident Response Agent** that improves over time by remembering past incidents using **Hindsight** memory.  
Instead of giving generic advice, it recalls similar resolved incidents and suggests targeted actions.

---

## Why this project?

Most LLM-based assistants are stateless unless you explicitly add memory.  
In incident management, memory is critical:

- What failed before?
- What actually fixed it?
- Which service patterns repeat?
- What should on-call engineers check first?

This project turns those lessons into machine-retrievable memory.

---

## What the agent does

The app supports a simple but effective loop:

1. **Create incident** with title, service, severity, symptoms, logs
2. **Diagnose incident** using:
   - current incident context
   - recalled historical memories from Hindsight
   - LLM reasoning (Groq API)
3. **Resolve incident** by recording root cause + resolution
4. **Retain learning** in memory for future similar incidents

Over time, diagnosis becomes faster and more context-aware.

---

## Tech stack

- **FastAPI** (backend APIs)
- **SQLite** (incident storage)
- **Groq LLM API** (diagnosis generation)
- **Hindsight** (memory retain + recall)
- Optional simple **HTML/CSS/JS frontend**

---

## Architecture overview

```text
[Frontend / Swagger]
        |
        v
 [FastAPI Endpoints]
   /incidents
   /incidents/{id}/diagnose
   /incidents/{id}/resolve
        |
        +--> [SQLite] incident records
        |
        +--> [Hindsight Recall] similar incidents
        |
        +--> [Groq LLM] diagnosis/action plan
        |
        +--> [Hindsight Retain] save resolved learnings
```

---

## API flow

### 1) Create incident
`POST /incidents`

Stores incident context.

### 2) Diagnose incident
`POST /incidents/{id}/diagnose`

- Build retrieval query from service + severity + symptoms + logs
- Recall top similar memories from Hindsight
- Build a structured prompt
- Ask LLM for:
  - likely root causes (max 3)
  - prioritized first 30-minute plan
  - fallback checks if first hypothesis fails

### 3) Resolve incident
`POST /incidents/{id}/resolve`

- Mark incident as resolved
- Save root cause + resolution
- Retain a memory document in Hindsight namespace

---

## Why Hindsight memory helps

Without memory, diagnosis is generic:
> “Check DB, check CPU, check logs…”

With memory, diagnosis is specific:
> “A similar checkout-service high-severity incident previously resolved by increasing DB pool size and tuning timeout after traffic surge; verify pool saturation first.”

This is exactly how experienced SREs think—based on historical patterns.

---

## Example before/after

### Incident #1
- Symptoms: p99 latency spike, DB pool timeout logs
- Resolution: increase pool size, tune timeout, restart pods
- Memory retained

### Incident #2 (similar)
- New diagnosis includes previous successful fix path
- Faster and more targeted triage

That demonstrates measurable agent learning behavior.

---

## Key implementation ideas

### Prompt strategy
Prompt includes:

- incident metadata
- logs/symptoms
- recalled memory snippets
- explicit output format instructions

This keeps response operational, not fluffy.

### Memory strategy
Retained memory includes:

- service
- severity
- symptoms/log signals
- root cause
- final resolution
- incident id metadata

### Safety strategy
- If Hindsight fails, continue with non-memory diagnosis
- If LLM key missing, return clear fallback message
- Store all incident states for auditability

---

## Challenges faced

1. **Python package compatibility (3.14)**
   - `pydantic-core` build errors
   - fixed by using Python 3.11/3.12

2. **Frontend-to-backend CORS**
   - browser preflight `OPTIONS` returning 405
   - fixed via FastAPI `CORSMiddleware`

3. **Environment mismatch**
   - `No module named fastapi/uvicorn`
   - resolved by installing dependencies in active virtual environment

---

## What’s next

- Similarity confidence scoring for recalled memories
- Runbook auto-linking per service
- Slack/Teams bot integration for on-call workflows
- Incident timeline ingestion from logs/APM tools
- Multi-tenant namespaces for team isolation

---

## Conclusion

This project shows that **memory is the missing layer** in AI incident tooling.  
By combining retrieval (Hindsight) + reasoning (LLM), we can move from generic assistant behavior to operationally useful incident guidance that improves with every resolution.

If you’re building AI for DevOps/SRE, start with this loop:

**Observe → Diagnose → Resolve → Remember → Reuse**

---

## Links

- Hindsight GitHub: https://github.com/vectorize-io/hindsight
- Hindsight Docs: https://hindsight.vectorize.io/
- Agent Memory Overview: https://vectorize.io/what-is-agent-memory
- FastAPI: https://fastapi.tiangolo.com/
- Groq API Docs: https://console.groq.com/docs
