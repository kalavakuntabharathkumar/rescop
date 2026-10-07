from statistics import mean, stdev
from .store import DocumentStore

def research(question: str, store: DocumentStore, top_k: int = 5) -> dict:
    # Explicit, inspectable workflow stages make this easy to extend to LangGraph.
    evidence = store.search(question, top_k=top_k)
    trace = [
        {"step": "retrieve", "status": "complete", "items": len(evidence)},
        {"step": "synthesize", "status": "complete", "method": "extractive evidence summary"},
        {"step": "quality_check", "status": "complete", "method": "evidence presence check"},
    ]
    if evidence:
        summary = "Evidence found in the indexed corpus. Review these source snippets before drawing conclusions."
        bullets = [{"source": item["title"], "snippet": item["snippet"], "relevance": item["score"]} for item in evidence]
    else:
        summary = "No matching evidence was found in the local corpus. Add relevant documents and run the query again."
        bullets = []
    return {"question": question, "summary": summary, "evidence": bullets, "trace": trace,
            "disclaimer": "Demo output; not investment advice and not a substitute for source verification."}

def risk_metrics(returns: list[float], annualization: int = 252) -> dict:
    avg = mean(returns)
    vol = stdev(returns)
    return {
        "observations": len(returns),
        "mean_period_return": round(avg, 8),
        "period_volatility": round(vol, 8),
        "annualized_volatility": round(vol * annualization ** 0.5, 8),
        "sharpe_like_ratio": round((avg / vol) * annualization ** 0.5, 4) if vol else None,
        "note": "Uses sample standard deviation and assumes returns are already decimal period returns."
    }
