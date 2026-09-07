# 🗺️ Roadmap de Evolução — Pesquisador Multi-Agente (Workflows)

Este roadmap define o plano de evolução técnica e de negócio para o **Pipeline Autônomo de Pesquisa e Redação Multi-Agente**, alimentado por LangGraph e Agent Harness.

---

## 📌 Fase 1: MVP Core (Concluída)
- [x] **Grafo de Estados LangGraph**: Estruturação de `ResearchState` com nós `researcher`, `writer` e `evaluator`.
- [x] **Subagentes Especializados**:
  - `ResearcherAgent`: Coleta e sanitização de evidências web.
  - `WriterAgent`: Síntese em Markdown e avaliação automática de qualidade.
- [x] **Agent Harness**: Ambiente controlado para testes determinísticos, auditoria JSON e asserção de transição de estados.
- [x] **Reuso de Infra**: Camada de resiliência LLM (`DynamicFallbackLLMManager`) e guardrails anti-injection (`validate_and_sanitize_query`).

---

## 🚀 Fase 2: Expansão de Agentes & Ferramentas (Próxima Sprint)
- [ ] **Subagente Revisor / Fact-Checker**:
  - Agente especializado em verificar declarações no rascunho contra a base de dados interna/Pinecone.
- [ ] **Integração com Vector DB (Pinecone)**:
  - Permitir que o `ResearcherAgent` consulte bases de conhecimento vetoriais locais além da web.
- [ ] **Multi-Format Exporter**:
  - Exportação automática de relatórios em PDF, HTML e JSON Estruturado.

---

## ⚡ Fase 3: Observabilidade & Interface Humano-no-Loop (Human-in-the-Loop)
- [ ] **Human-in-the-Loop (Interrupts no LangGraph)**:
  - Adicionar nó de aprovação humana caso o `quality_score` permaneça abaixo do limiar após 2 revisões.
- [ ] **Dashboard de Observabilidade (LangSmith / MLflow)**:
  - Telemetria em tempo real de latência, custo de tokens e gráfico de transição de estados.
- [ ] **API REST (FastAPI)**:
  - Interface HTTP assíncrona com suporte a streaming SSE do progresso dos agentes.

---

## 🔒 Fase 4: Produção & Escala
- [ ] **Deploy em Container GCP Cloud Run**:
  - Containerização e deploy serverless da API de orquestração.
- [ ] **Trabalhos Agendados (Cloud Scheduler)**:
  - Pesquisa e geração de relatórios periódicos em segundo plano com notificações no Slack/Discord.

---

## 📊 Matriz de Priorização (Esforço x Impacto)

```
          ALTO IMPACTO
               │
    [Fase 2: Fact-Checker]    [Fase 3: Human-in-the-Loop]
               │
BAIXO ─────────┼────────── HEAVY
ESFORÇO        │           ESFORÇO
               │
    [Fase 2: Multi-Export]    [Fase 4: GCP Cloud Run]
               │
          BAIXO IMPACTO
```
