# Automação de Mensagem Motivacional Diária

Este projeto contém um workflow do n8n que automatiza o envio de mensagens inspiradoras para o Telegram, utilizando a API do Google Gemini para gerar conteúdos originais e curtos todas as manhãs.

## Como Funciona

O workflow segue o seguinte fluxo de execução:

1.  **Agendamento**: O gatilho é disparado automaticamente todos os dias às **08:00** (horário de Brasília).
2.  **Configuração**: Um nó do tipo `Set` define variáveis estáticas, como o ID do chat do Telegram.
3.  **IA (Gemini)**: Uma requisição HTTP é feita para a API `gemini-1.5-flash` com um prompt específico para gerar uma mensagem curta, positiva e com emojis.
4.  **Entrega**: A mensagem gerada é enviada via bot para o chat configurado no Telegram.

## Estrutura do Workflow

*   **Agendamento Diário**: Trigger do tipo `Schedule`.
*   **Configurações**: Define o `chatId`.
*   **Gerar Mensagem (Gemini)**: Nó `HTTP Request` que interage com a API Generative Language do Google.
*   **Enviar para Telegram**: Nó `Telegram` para envio da resposta final.

!Screenshot do Workflow

## Pré-requisitos

Para que este workflow funcione, você precisará de:

1.  **n8n instalado** (via Docker ou Desktop).
2.  **API Key do Google Gemini**: Obtida no Google AI Studio.
3.  **Bot no Telegram**: Criado via `@BotFather`.
4.  **Chat ID**: O ID do chat (pessoal ou grupo) para onde as mensagens serão enviadas.

## Configuração

1.  Importe o arquivo `n8n.json` para o seu n8n.
2.  No nó **Configurações**, substitua `SEU_CHAT_ID_AQUI` pelo seu ID real.
3.  No nó **Gerar Mensagem (Gemini)**, em *Query Parameters*, substitua `SUA_API_KEY_DO_GEMINI_AQUI` pela sua chave da API do Google.
4.  Configure as credenciais no nó **Enviar para Telegram** com o seu Bot Token.
5.  Ative o workflow (Active: ON).

---
*Projeto desenvolvido como parte dos estudos de Dados e Automações.*