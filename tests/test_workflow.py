from app.store import DocumentStore
from app.workflow import research, risk_metrics

def test_research_returns_evidence():
    store = DocumentStore()
    store.add("Inflation memo", "Inflation remains a key risk as credit conditions tighten across sectors.")
    result = research("inflation credit", store)
    assert len(result["evidence"]) == 1
    assert result["trace"][0]["step"] == "retrieve"

def test_research_empty_corpus():
    result = research("unknown question", DocumentStore())
    assert result["evidence"] == []
    assert "No matching evidence" in result["summary"]

def test_risk_metrics():
    result = risk_metrics([0.01, -0.005, 0.02, 0.0], annualization=252)
    assert result["observations"] == 4
    assert result["annualized_volatility"] > 0
