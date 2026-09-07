import json
import logging
import time
from typing import Dict, Any, List, Optional
from graph.workflow import build_research_graph
from graph.state import ResearchState

class AgentHarness:
    """Agent Harness: Ambiente controlado para testes, auditoria e execução de workflows multi-agente."""

    def __init__(self, graph=None):
        self.graph = graph or build_research_graph()
        self.last_state: Optional[ResearchState] = None
        self.execution_duration: float = 0.0

    def run(self, topic: str, initial_state_override: Optional[Dict[str, Any]] = None) -> ResearchState:
        """Executa o pipeline multi-agente monitorando a transição de estados."""
        start_time = time.time()

        initial_state: ResearchState = {
            "topic": topic,
            "research_queries": [],
            "raw_evidence": [],
            "draft": "",
            "final_report": "",
            "quality_score": 0.0,
            "revision_count": 0,
            "execution_logs": [],
            "status": "SEARCHING"
        }

        if initial_state_override:
            initial_state.update(initial_state_override)

        logging.info(f"Harness: Iniciando execução para o tema '{topic}'...")
        final_output = self.graph.invoke(initial_state)

        self.execution_duration = time.time() - start_time
        self.last_state = final_output
        logging.info(f"Harness: Execução concluída em {self.execution_duration:.2f}s. Status: {final_output.get('status')}")

        return final_output

    def get_execution_steps(self) -> List[str]:
        """Retorna a sequência de passos registrados nos logs."""
        if not self.last_state:
            return []
        return [log["step"] for log in self.last_state.get("execution_logs", [])]

    def assert_state_transition(self, expected_steps: List[str]) -> bool:
        """Valida se a sequência executada contém a sequência de passos esperada."""
        actual_steps = self.get_execution_steps()
        logging.info(f"Harness Assert: Esperado={expected_steps}, Obtido={actual_steps}")

        for expected in expected_steps:
            if expected not in actual_steps:
                raise AssertionError(f"Passo esperado '{expected}' não foi executado. Passos executados: {actual_steps}")
        return True

    def export_audit_log(self, filepath: str) -> str:
        """Exporta os logs de auditoria e métricas para um arquivo JSON."""
        if not self.last_state:
            raise ValueError("Nenhuma execução realizada para exportar logs.")

        audit_data = {
            "topic": self.last_state.get("topic"),
            "duration_seconds": self.execution_duration,
            "status": self.last_state.get("status"),
            "quality_score": self.last_state.get("quality_score"),
            "revision_count": self.last_state.get("revision_count"),
            "steps": self.get_execution_steps(),
            "logs": self.last_state.get("execution_logs", []),
            "evidence_count": len(self.last_state.get("raw_evidence", [])),
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(audit_data, f, indent=2, ensure_ascii=False)

        return filepath
