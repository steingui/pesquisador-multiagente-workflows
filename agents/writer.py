import datetime
import logging
from typing import Dict, Any, Optional
from graph.state import ResearchState, LogEntry
from core.llm_factory import DynamicFallbackLLMManager
from langchain_core.messages import SystemMessage, HumanMessage

class WriterAgent:
    """Subagente Redator: Consolida evidências e escreve o relatório final em Markdown."""

    def __init__(self, llm_manager: Optional[DynamicFallbackLLMManager] = None):
        self.llm_manager = llm_manager or DynamicFallbackLLMManager()

    def generate_report(self, topic: str, evidence_list: list) -> str:
        """Gera o relatório estruturado em Markdown."""
        evidence_text = ""
        sources = []
        for idx, ev in enumerate(evidence_list, 1):
            evidence_text += f"\n--- Evidência {idx} ---\nTítulo: {ev['title']}\nConteúdo: {ev['body']}\nFonte: {ev['source']}\n"
            if ev.get("url"):
                sources.append(f"- [{ev['title']}]({ev['url']}) ({ev['source']})")
            else:
                sources.append(f"- {ev['title']} ({ev['source']})")

        prompt = [
            SystemMessage(content=(
                "Você é um redator sênior técnico e analítico. Escreva um relatório completo em Markdown sobre o tema fornecido. "
                "Utilize as evidências disponibilizadas sem inventar dados não comprovados. "
                "O relatório DEVE conter as seções:\n"
                "# Relatório Executivo: [Tema]\n"
                "## 1. Introdução\n"
                "## 2. Principais Achados e Evidências\n"
                "## 3. Análise Crítica e Conclusão\n"
                "## 4. Referências e Fontes Consultadas"
            )),
            HumanMessage(content=f"Tema: {topic}\n\nEvidências:\n{evidence_text}")
        ]

        try:
            response = self.llm_manager.invoke_with_fallback(prompt)
            report = response.content
            if "## 4. Referências" not in report and sources:
                report += "\n\n## 4. Referências e Fontes Consultadas\n" + "\n".join(sources)
            return report
        except Exception as e:
            logging.warning(f"Erro ao gerar relatório via LLM: {e}. Usando template de fallback.")
            fontes_formatted = "\n".join(sources) if sources else "- Fonte interna de pesquisa."
            return (
                f"# Relatório Executivo: {topic}\n\n"
                f"## 1. Introdução\n"
                f"Este relatório consolida a análise sobre **{topic}** com base nas evidências levantadas.\n\n"
                f"## 2. Principais Achados e Evidências\n"
                f"{evidence_text}\n\n"
                f"## 3. Análise Crítica e Conclusão\n"
                f"As informações apontam para relevância direta do tema no contexto atual.\n\n"
                f"## 4. Referências e Fontes Consultadas\n"
                f"{fontes_formatted}"
            )

    def evaluate_quality(self, report: str) -> float:
        """Avalia a qualidade do relatório baseado em estrutura e extensão."""
        score = 0.5
        if len(report) > 300:
            score += 0.2
        if "## 1. Introdução" in report:
            score += 0.1
        if "## 2. Principais" in report:
            score += 0.1
        if "## 4. Referências" in report or "Fontes" in report:
            score += 0.1
        return min(score, 1.0)

    def run(self, state: ResearchState) -> Dict[str, Any]:
        """Nó do LangGraph para o subagente Redator."""
        topic = state["topic"]
        evidence = state.get("raw_evidence", [])

        report = self.generate_report(topic, evidence)
        score = self.evaluate_quality(report)

        now = datetime.datetime.now().isoformat()
        log_entry: LogEntry = {
            "step": "WriterAgent",
            "timestamp": now,
            "message": f"Relatório gerado com sucesso. Quality Score: {score:.2f}.",
            "details": {"report_length": len(report), "quality_score": score}
        }

        logs = list(state.get("execution_logs", []))
        logs.append(log_entry)

        status = "COMPLETED" if score >= 0.7 or state.get("revision_count", 0) >= 2 else "REVISING"

        return {
            "draft": report,
            "final_report": report,
            "quality_score": score,
            "execution_logs": logs,
            "status": status
        }
