from agents.researcher import ResearcherAgent
from graph.state import ResearchState

def test_researcher_run():
    agent = ResearcherAgent()
    state: ResearchState = {
        "topic": "Inteligência Artificial na Educação",
        "research_queries": [],
        "raw_evidence": [],
        "draft": "",
        "final_report": "",
        "quality_score": 0.0,
        "revision_count": 0,
        "execution_logs": [],
        "status": "SEARCHING"
    }

    result = agent.run(state)
    assert "raw_evidence" in result
    assert len(result["raw_evidence"]) > 0
    assert result["status"] == "DRAFTING"
    assert len(result["execution_logs"]) == 1
