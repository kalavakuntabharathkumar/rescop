# Agentic AI Research Copilot for Analysts

A local-first research assistant demo with a FastAPI backend, document ingestion, TF-IDF retrieval, lightweight multi-step research workflow, risk statistics, and a React-free static dashboard served by FastAPI. It runs without paid model credentials; an optional LLM provider can be added behind the explanation interface. It does not claim to index 1.2M documents or deliver benchmarked CUDA performance.

## Features
- Upload plain-text/Markdown research documents
- Search corpus with ranked TF-IDF retrieval and snippets
- Multi-step research plan: retrieve evidence, summarize themes, calculate simple return-risk statistics from CSV, and produce a trace
- Redis cache support is optional; local in-memory fallback works without Redis
- Health and metrics-friendly API layout
- Pytest unit tests and GitHub Actions CI

## Run
Python 3.11+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` and API docs at `/docs`.

## Endpoints
- `POST /api/documents` — add a document JSON body `{ "title": "...", "text": "...", "source": "..." }`
- `GET /api/search?q=inflation&top_k=5` — ranked retrieval
- `POST /api/research` — run the research workflow for a question
- `POST /api/risk` — calculate mean return, volatility, and Sharpe-like ratio from a list of returns
- `GET /health` — health status

## Notes
This project intentionally uses transparent local retrieval and deterministic explanations so it works out of the box. Production use would require document connectors, authentication, authorization, audit logging, PII controls, model evaluations, prompt-injection defenses, and measured load tests.
