# AGENTS.md — Contrato de Governança para Pesquisador Multi-Agente (Workflows)

## 1 Fonte de Verdade
- Runtime: Python 3.11+
- Dependências: `requirements.txt`
- Orquestração: LangGraph StateGraph
- Testes: `pytest tests/ -q`

## 2 Estrutura do Projeto
```
pesquisador-multiagente-workflows/
├── agents/         # Subagentes (researcher, writer)
├── graph/          # Definição de estados e workflow LangGraph
├── harness/        # Agent Harness para testes, logs e controle
├── core/           # LLM factory e guardrails reutilizados
├── tests/          # Suíte de testes automatizados
├── main.py         # Entrypoint CLI
└── ROADMAP.md      # Roadmap de evolução do projeto
```

## 3 Execução de Testes
```bash
pytest tests/ -q
```
