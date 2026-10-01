from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
from .models import DocumentIn, ResearchRequest, RiskRequest
from .store import store
from .workflow import research, risk_metrics

app = FastAPI(title="Agentic AI Research Copilot", version="0.1.0",
              description="Local research workflow demo with transparent retrieval.")

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return (Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status": "ok", "documents": len(store.all())}

@app.post("/api/documents", status_code=201)
def add_document(body: DocumentIn):
    return store.add(body.title, body.text, body.source)

@app.get("/api/documents")
def list_documents():
    return [{"id": d.id, "title": d.title, "source": d.source, "characters": len(d.text)} for d in store.all()]

@app.get("/api/search")
def search(q: str, top_k: int = 5):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    if not 1 <= top_k <= 10:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 10")
    return {"query": q, "results": store.search(q, top_k)}

@app.post("/api/research")
def run_research(body: ResearchRequest):
    return research(body.question, store, body.top_k)

@app.post("/api/risk")
def calculate_risk(body: RiskRequest):
    if len(body.returns) < 2:
        raise HTTPException(status_code=400, detail="At least two returns are required")
    return risk_metrics(body.returns, body.annualization)
