#  SOC Investigator - AI-Powered Triage Tool

##  Objetivo do Projeto
Desenvolver uma interface de triagem rápida para analistas de SOC, integrando um Frontend em **Streamlit** a um Agente de Inteligência Artificial orquestrado no **n8n**. O objetivo é automatizar a investigação de IPs e URLs, reduzindo o tempo de resposta a incidentes (MTTR) através de automação inteligente.

##  Arquitetura da Solução
A solução utiliza o conceito de desacoplamento entre interface e lógica de negócio:
1. **Interface (Frontend):** Aplicação Streamlit que coleta o IOC (Indicator of Compromise) e dispara o gatilho.
2. **Orquestração (Backend):** Workflow no n8n que recebe o Webhook e gerencia o fluxo de decisão.
3. **Inteligência (Agentic):** IA baseada no modelo `gpt-4o-mini` que processa dados brutos e gera inteligência de ameaças.
4. **Contrato de Resposta:** Saída padronizada em JSON para garantir a integridade da UI.

##  Stack Técnica
- **Linguagem:** Python 3.11+
- **Bibliotecas Chave:** `streamlit`, `requests`, `python-dotenv`
- **Orquestração:** n8n (Self-hosted/Docker)
- **LLM:** OpenAI GPT-4o-mini
- **Infraestrutura:** Segredos gerenciados via `.env` (em conformidade com práticas de segurança).

##  Contrato da API (Webhook n8n)
Para que o frontend processe a resposta corretamente, o nó `Respond to Webhook` do n8n deve seguir este esquema JSON:

```json
{
  "verdict": "Seguro | Suspeito | Malicioso",
  "reason": "Descrição técnica detalhada da análise."
}
```

##  Instalação e Execução

### 1. Requisitos Prévios
- Python 3.11+ instalado.
- Instância do n8n ativa.

### 2. Configuração do Ambiente
Crie um ambiente virtual e instale as dependências:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente
Configure o arquivo `.env` na raiz do projeto (nunca versione este arquivo):
```env
OPENAI_API_KEY=sua_chave_aqui
N8N_WEBHOOK_URL=http://seu-ip:5678/webhook/sua-rota
```

### 4. Execução
```bash
streamlit run apps/05_soc_investigator.py
```

##  Notas de Engenharia e Governança
- **Tratamento de Erros:** O sistema implementa timeouts de 30s para evitar travamentos da UI em caso de falha no backend.
- **Segurança:** O uso do `.gitignore` garante que credenciais de API não sejam expostas em repositórios públicos.
- **Depuração:** Resolvido o problema de resposta assíncrona do n8n utilizando o nó `Respond to Webhook`, garantindo que o Streamlit aguarde a conclusão da análise da IA antes de renderizar o veredito.

##  Roadmap
- [ ] Implementar logs de auditoria em banco de dados SQL (Compliance).
- [ ] Adicionar suporte a análise de hashes (SHA256).
- [ ] Autenticação via OAuth2 para acesso à interface.