import sys
import os
import argparse
import logging
from dotenv import load_dotenv
from harness.agent_harness import AgentHarness
from core.guardrails import validate_and_sanitize_query

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Pipeline Autônomo de Pesquisa e Redação Multi-Agente (LangGraph)")
    parser.add_argument("--topic", type=str, help="Tema para pesquisa e redação do relatório", default="Reforma Tributária e Impacto na Cesta Básica no Brasil")
    parser.add_argument("--output", type=str, help="Arquivo de saída para o relatório final em Markdown", default="relatorio_final.md")
    parser.add_argument("--audit", type=str, help="Arquivo JSON de saída para a trilha de auditoria", default="audit_log.json")

    args = parser.parse_args()

    try:
        clean_topic = validate_and_sanitize_query(args.topic)
    except ValueError as err:
        print(f"Erro de Validação: {err}")
        sys.exit(1)

    print(f"\n🚀 Iniciando Pipeline Autônomo de Pesquisa Multi-Agente...")
    print(f"📌 Tema: '{clean_topic}'\n")

    harness = AgentHarness()
    result = harness.run(clean_topic)

    report = result.get("final_report", "")
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report)

    audit_path = harness.export_audit_log(args.audit)

    print(f"\n✅ Pipeline concluído com sucesso!")
    print(f"📄 Relatório salvo em: {args.output}")
    print(f"📊 Trilha de auditoria salva em: {audit_path}")
    print(f"⭐ Score de Qualidade: {result.get('quality_score', 0.0):.2f}")
    print(f"🔄 Total de Revisões: {result.get('revision_count', 0)}")

if __name__ == "__main__":
    main()
