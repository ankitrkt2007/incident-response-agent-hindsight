# Incident Response Agent using Hindsight

An AI Incident Response Agent that learns from past incidents using Hindsight memory.  
It recalls similar outages and suggests faster, context-aware remediation.

## Features
- Create incidents with symptoms/logs
- Diagnose incidents with LLM + memory recall
- Resolve incidents and store lessons into Hindsight
- Show before/after behavior improvement with memory

## Tech Stack
- FastAPI
- SQLite
- Groq LLM API
- Hindsight memory

## Setup

1. Clone/download this project
2. Create virtual environment
3. Install dependencies
4. Add `.env` file from `.env.example`
5. Run server

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
