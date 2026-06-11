```text
██╗  ██╗ █████╗ ███╗   ██╗███████╗███████╗██╗
██║ ██╔╝██╔══██╗████╗  ██║██╔════╝██╔════╝██║
█████╔╝ ███████║██╔██╗ ██║███████╗█████╗  ██║
██╔═██╗ ██╔══██║██║╚██╗██║╚════██║██╔══╝  ██║
██║  ██╗██║  ██║██║ ╚████║███████║███████╗██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝
```

# Kensei AI Foundations: Engenharia de Dados & Automação Inteligente

##  Sobre o Programa & Ecossistema
Este repositório consolida o desenvolvimento técnico e a arquitetura de soluções criadas durante o programa **Kensei AI Foundations**. Sob a égide do **Kensei CyberSec Lab** — uma instituição com mais de 20 anos de expertise em tecnologia e segurança — este projeto foi estruturado sob a mentalidade "Precisão de Samurai": a busca por pipelines impecáveis, pipelines estáveis e arquiteturas "AI-First".

O foco central não é apenas a codificação passiva, mas a aplicação de engenharia de valor para resolver problemas reais de negócios, transformando dados brutos em ativos estratégicos e tarefas manuais em fluxos autônomos de alta disponibilidade.

##  O Que Vou Aprender?

A trilha técnica é dividida em blocos lógicos de competências, garantindo uma progressão que vai do código assistido à orquestração de sistemas complexos:

| Tópico | Descrição |
| :--- | :--- |
| 🤖 **IA como Copiloto** | Domínio de Prompt Engineering e integração de LLMs no fluxo de trabalho diário. |
| 🐍 **Python do Zero** | Lógica de programação e desenvolvimento de scripts com suporte de IA generativa. |
| 📊 **Dados & Análise** | Manipulação profunda com Pandas, visualização de dados e geração de insights reais. |
| 🔌 **APIs de IA** | Integração programática com modelos de ponta como OpenAI e Claude. |
| ⚙️ **Automação n8n** | Construção de workflows inteligentes combinando no-code com IA em ambiente self-hosted. |
| 🌐 **Apps com Streamlit** | Desenvolvimento de aplicações web rápidas e funcionais para entrega de valor ao usuário. |

##  Arquitetura de Soluções (Data & Automation Pipelines)

O projeto é dividido em duas esteiras principais que demonstram maturidade técnica em diferentes camadas da pilha tecnológica:

### 1. Módulo de Engenharia e Análise de Dados
Focado no ciclo de vida do dado, desde a ingestão até a geração de insights executivos.
*   **Propósito Técnico**: Implementação de pipelines de ETL (Extract, Transform, Load) utilizando Python.
*   **Manipulação de Dados**: Uso intensivo da biblioteca **Pandas** para limpeza, normalização e agregação de grandes volumes de informação.
*   **Ganho Operacional**: Redução drástica no tempo de processamento de relatórios e eliminação de erros humanos em análises estatísticas complexas, permitindo uma tomada de decisão baseada em dados reais.

### 2. Módulo de Automação de Processos (Pipeline-as-Code)
Demonstra a capacidade de orquestrar ferramentas e APIs em um ecossistema integrado.
*   **Propósito Técnico**: Desenvolvimento de fluxos lógicos em ambiente self-hosted utilizando **n8n**.
*   **Integrações**: Consumo de APIs REST, configuração de Webhooks e tratamento de fluxos de decisão complexos (nós condicionais e loops).
*   **Persistência e Notificação**: Centralização de dados estruturados em bases relacionais (ou ferramentas como Baserow) com camadas de notificação automatizada para monitoramento em tempo real.

##  Infraestrutura e Stack Tecnológica

A escolha das ferramentas reflete uma preocupação com o isolamento de ambientes e a reprodutibilidade em cenários de produção.

| Tecnologia | Aplicação Técnica | Diferencial de Engenharia |
| :--- | :--- | :--- |
| **Linux/WSL** | Sistema Operacional | Ambiente de desenvolvimento padronizado e otimizado para servidores. |
| **Docker** | Conteinerização | Garantia de que as ferramentas (n8n, bancos de dados) rodem de forma isolada e idêntica em qualquer host. |
| **Python & Pandas** | Data Processing | Manipulação de alta performance para estruturação de DataFrames e lógica de IA. |
| **n8n** | Orquestração | Workflow engine para automação de processos críticos sem lock-in de fornecedor. |
| **Git/GitHub** | Versionamento | Histórico de desenvolvimento utilizando padrões de Conventional Commits. |

##  Diferenciais Técnicos e Mentalidade de Produção

Como engenheiro focado em resultados, este repositório adota três pilares indispensáveis para qualquer ambiente corporativo moderno:

1.  **Segurança e Governança de Dados**: 
    *   Implementação de gestão de segredos (Secrets Management).
    *   Nenhuma credencial ou chave de API é exposta no código; uso rigoroso de variáveis de ambiente (`.env`).
    *   Conformidade com princípios de privacidade e integridade dos dados manipulados.

2.  **Tratamento de Erros e Resiliência**: 
    *   Lógica de "Error Handling" embutida nos fluxos de automação para evitar paradas sistêmicas.
    *   Implementação de logs para rastreabilidade de falhas em processos críticos.

3.  **Eficiência Operacional**: 
    *   Substituição de processos manuais repetitivos por agentes autônomos que operam em regime 24/7 com supervisão mínima.
    *   Arquitetura escalável que permite a adição de novos módulos sem degradar a performance do sistema existente.

##  DESTAQUE PRINCIPAL: RELATÓRIO FINAL
Para uma visão detalhada da minha evolução, arquitetura de soluções e análise técnica de cada semana, acesse:
👉 [CLIQUE AQUI PARA VER O RELATÓRIO COMPLETO (PDF)](./docs/relatorio_final_tulani.pdf)

---
##  Instalação e Execução

Para validar os pipelines e o ambiente de desenvolvimento, siga as instruções abaixo:

### Pré-requisitos
*   Docker & Docker Compose instalados.
*   Python 3.12+ (recomendado uso de venv).

### Passo a Passo

1.  **Clonar o Repositório**:
    ```bash
    git clone https://github.com/seu-usuario/Dados_e_automacoes.git
    cd Dados_e_automacoes
    ```

2.  **Subir Infraestrutura (Self-hosted)**:
    ```bash
    docker-compose up -d
    ```

3.  **Configurar Ambiente Python**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    pip install -r requirements.txt
    ```

4.  **Importar Fluxos**:
    Os arquivos `.json` das automações podem ser importados diretamente na sua instância local do n8n para auditoria técnica.

---
*Este projeto é um registro da evolução técnica e do compromisso com a excelência em engenharia de dados e IA no Kensei CyberSec Lab.*