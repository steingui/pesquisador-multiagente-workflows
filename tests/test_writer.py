from agents.writer import WriterAgent
from graph.state import ResearchState

def test_writer_run():
    agent = WriterAgent()
    state: ResearchState = {
        "topic": "Energia Renovável",
        "research_queries": ["energia solar", "energia eólica"],
        "raw_evidence": [
            {"title": "Avancos Solares", "body": "Crescimento de 30% em 2025.", "url": "https://solar.org", "source": "Web"}
        ],
        "draft": "",
        "final_report": "",
        "quality_score": 0.0,
        "revision_count": 0,
        "execution_logs": [],
        "status": "DRAFTING"
    }

    result = agent.run(state)
    assert "draft" in result
    assert "# Relatório Executivo: Energia Renovável" in result["draft"]
    assert result["quality_score"] > 0.5
