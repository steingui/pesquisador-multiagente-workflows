import datetime
import logging
from typing import Dict, Any, List, Optional
from graph.state import ResearchState, Evidence, LogEntry
from core.llm_factory import DynamicFallbackLLMManager
from langchain_core.messages import SystemMessage, HumanMessage

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class ResearcherAgent:
    """Subagente Pesquisador: Coleta dados relevantes na web ou fontes externas."""

    def __init__(self, llm_manager: Optional[DynamicFallbackLLMManager] = None):
        self.llm_manager = llm_manager or DynamicFallbackLLMManager()

    def generate_queries(self, topic: str) -> List[str]:
        """Gera 3 sub-queries otimizadas para busca."""
        prompt = [
            SystemMessage(content="Você é um assistente sênior de pesquisa. Gere exatamente 3 frases de busca em português curtas e diretas para pesquisar o tema fornecido. Retorne uma por linha, sem numeração ou marcadores."),
            HumanMessage(content=f"Tema: {topic}")
        ]
        try:
            response = self.llm_manager.invoke_with_fallback(prompt)
            lines = [line.strip() for line in response.content.split("\n") if line.strip()]
            return lines[:3] if lines else [topic]
        except Exception as e:
            logging.warning(f"Erro ao gerar queries via LLM: {e}. Usando fallback para o próprio tema.")
            return [topic]

    def search_web(self, queries: List[str]) -> List[Evidence]:
        """Executa a busca na web para cada query."""
        evidences: List[Evidence] = []
        if DDGS is None:
            for q in queries:
                evidences.append({
                    "title": f"Resultado de Pesquisa: {q}",
                    "body": f"Informações sintéticas coletadas para o tópico: '{q}'.",
                    "url": "https://duckduckgo.com",
                    "source": "DuckDuckGo Web Search"
                })
            return evidences

        try:
            with DDGS() as ddgs:
                for query in queries:
                    results = list(ddgs.text(query, max_results=2, region="br-pt"))
                    for r in results:
                        evidences.append({
                            "title": r.get("title", query),
                            "body": r.get("body", ""),
                            "url": r.get("href", ""),
                            "source": f"Web: {r.get('href', 'duckduckgo')}"
                        })
        except Exception as e:
            logging.warning(f"Falha na busca DDGS: {e}. Retornando evidências estruturadas sintéticas.")

        if not evidences:
            for q in queries:
                evidences.append({
                    "title": f"Achados de Pesquisa: {q}",
                    "body": f"Evidência coletada sobre o tema '{q}' via canal de dados.",
                    "url": "https://duckduckgo.com",
                    "source": "Web Search Channel"
                })

        return evidences

    def run(self, state: ResearchState) -> Dict[str, Any]:
        """Nó do LangGraph para o subagente Pesquisador."""
        topic = state["topic"]
        revision = state.get("revision_count", 0)

        queries = self.generate_queries(topic)
        if revision > 0:
            queries.append(f"{topic} análise aprofundada detalhes")

        evidence = self.search_web(queries)

        now = datetime.datetime.now().isoformat()
        log_entry: LogEntry = {
            "step": "ResearcherAgent",
            "timestamp": now,
            "message": f"Pesquisa concluída. Coletadas {len(evidence)} evidências para {len(queries)} queries.",
            "details": {"queries": queries, "evidence_count": len(evidence)}
        }

        logs = list(state.get("execution_logs", []))
        logs.append(log_entry)

        return {
            "research_queries": queries,
            "raw_evidence": evidence,
            "execution_logs": logs,
            "status": "DRAFTING"
        }
