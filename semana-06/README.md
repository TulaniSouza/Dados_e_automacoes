# Projeto Data Product - Semana 06

## Objetivo do produto
Definir e entregar um pipeline de decisão de agente de dados com foco em valor executivo, não apenas uma demo técnica.

### North Star sugerido
- Reduzir tempo de triagem SOC em 40%
- Aumentar qualidade de investigação de IOC com evidência auditável

## Arquitetura 3 camadas
1. Orquestração
   - n8n para orquestrar gatilhos, agentes e integração com ferramentas.
   - Workflow documentado por agente.
2. Dados
   - Persistência de entrada, decisões, logs de tool, custo e latência.
   - Banco SQL (Postgres recomendado) para consulta e auditoria.
3. Governança
   - Versionamento de prompts.
   - Controle de chaves/API.
   - Limites de iteração e trilha de auditoria.

## Estrutura de pastas
- `n8n/`: workflows exportados e templates de orquestração.
- `prompts/`: prompt versionado e metadata.
- `schemas/`: contratos de dados de entrada e saída por agente.
- `scripts/`: scripts de ingestão, avaliação e replay.
- `data/`: datasets versionados e golden set.
- `exports/`: arquivos JSON exportados por agente.
- `report-executivo.md`: relatório executivo de 1 página.

## Fases do projeto
- Fase 1: agente com log completo.
- Fase 2: agente CSV com dataset real e perguntas de negócio.
- Fase 3: agente SOC triagem com classificação, justificativa e evidência.
- Fase 4: hardening, avaliação, custo, segurança e empacotamento.

## Riscos e decisões técnicas
- Não instrumentar logs de decisão torna o projeto não auditável.
- Sem data contracts, o produto não escala e não garante qualidade.
- Fallback obrigatório para APIs externas evita falhas de disponibilidade.
- Prompts devem ser versionados e revisados como código.

## Arquitetura
- Arquitetura de Operações (LLMOps): Este projeto implementa uma separação de responsabilidades para garantir a auditabilidade do agente:
- Orquestração: Implementada em n8n para agilidade na integração de ferramentas e memória.
- Governança: Registry de prompts em JSON para controle de versionamento e rastreabilidade de comportamento.
- Validação (QA): Scripts Python dedicados para validação de integridade de dados (SHA256) e medição de acurácia via Golden Sets, garantindo que as decisões do agente sejam consistentes e auditáveis.

## Entregáveis
- Quatro JSONs de exporte por agente em `exports/`.
- `README.md` com arquitetura, riscos, custos e decisões.
- `report-executivo.md` com impacto, limite atual e próximos investimentos.

## Como rodar localmente
1. Crie/ative um ambiente Python.
2. Instale dependências:
```powershell
pip install -r requirements.txt
```
3. Execute a ingestão de CSV de exemplo:
```powershell
python scripts\ingest_csv.py data\sample_input.csv --output-path data\
```
4. Avalie o golden set de exemplo:
```powershell
python scripts\evaluate_golden_set.py golden\golden_set_example.json exports\sample_agent_results.json
```
5. Para reproduzir decisões, implemente a lógica em `scripts/replay_decision.py`.
