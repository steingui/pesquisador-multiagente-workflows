import datetime
from typing import Dict, Any, Literal
from langgraph.graph import StateGraph, START, END
from graph.state import ResearchState, LogEntry
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent

researcher_agent = ResearcherAgent()
writer_agent = WriterAgent()

def researcher_node(state: ResearchState) -> Dict[str, Any]:
    return researcher_agent.run(state)

def writer_node(state: ResearchState) -> Dict[str, Any]:
    return writer_agent.run(state)

def evaluator_node(state: ResearchState) -> Dict[str, Any]:
    """Nó avaliador de transição para decidir se aprova o relatório ou faz nova rodada."""
    score = state.get("quality_score", 0.0)
    revisions = state.get("revision_count", 0)

    now = datetime.datetime.now().isoformat()
    if score >= 0.7 or revisions >= 2:
        new_status = "COMPLETED"
        msg = f"Fluxo finalizado. Score de qualidade ({score:.2f}) atingiu o limite ou máximo de revisões ({revisions}) alcançado."
    else:
        new_status = "REVISING"
        msg = f"Relatório precisa de revisão. Score: {score:.2f}, iniciando revisão {revisions + 1}."

    log_entry: LogEntry = {
        "step": "EvaluatorNode",
        "timestamp": now,
        "message": msg,
        "details": {"quality_score": score, "revisions": revisions, "new_status": new_status}
    }

    logs = list(state.get("execution_logs", []))
    logs.append(log_entry)

    return {
        "revision_count": revisions + 1 if new_status == "REVISING" else revisions,
        "execution_logs": logs,
        "status": new_status
    }

def route_next(state: ResearchState) -> Literal["researcher", "__end__"]:
    """Condicional para direcionar o próximo nó."""
    if state.get("status") == "COMPLETED":
        return END
    return "researcher"

def build_research_graph():
    """Constrói e compila o grafo de estados LangGraph."""
    builder = StateGraph(ResearchState)

    builder.add_node("researcher", researcher_node)
    builder.add_node("writer", writer_node)
    builder.add_node("evaluator", evaluator_node)

    builder.add_edge(START, "researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "evaluator")

    builder.add_conditional_edges("evaluator", route_next)

    return builder.compile()
