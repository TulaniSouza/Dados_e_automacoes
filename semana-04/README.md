# Projeto Semana 04: Automação com IA

Este projeto contém 5 ferramentas de automação utilizando APIs de IA (GitHub Models) para processar dados, gerar relatórios e interagir com usuários.

## Funcionalidades

### 1. Consulta Simples à IA (`01_hello_api.py`)
- Faz perguntas diretas para o modelo GPT-4o-mini
- Interface simples via terminal

### 2. Assistente Conversacional (`02_assistente.py`)
- Chatbot especialista em cibersegurança
- Mantém histórico de conversa
- Respostas em português brasileiro

### 3. Analisador de Texto (`03_analisador.py`)
- Analisa textos fornecidos pelo usuário
- Gera resumos, identifica temas e sentimentos
- Salva análises em `data/outputs/analise_saida.md`

### 4. Tradutor de Idiomas (`04_tradutor.py`)
- Traduz textos para qualquer idioma
- Detecta idioma automaticamente
- Salva traduções em `data/outputs/ultima_traducao.txt`

### 5. Gerador de Relatórios (`05_gerador_relatorios.py`)
- Lê dados CSV de `data/inputs/dados.csv`
- Gera relatórios Markdown automatizados
- Inclui estatísticas e insights

### 6. Teste API Claude (`06_teste_claude.py`)
- Testa integração com Anthropic Claude
- Comparação entre modelos (opcional)

### 7. Ferramenta Integrada (`07_ferramenta_integrada.py`)
- Menu unificado para acessar todas as funcionalidades
- Interface centralizada e fácil de usar

## Como Usar

### Pré-requisitos
- Python 3.8+
- Ambiente virtual configurado
- Token do GitHub Models

### Instalação
```bash
# Clonar repositório
git clone https://github.com/TulaniSouza/Dados_e_automacoes.git
cd semana-04

# Instalar dependências
pip install -r requirements.txt

# Configurar ambiente
cp .env.example .env
# Editar .env com seu GITHUB_TOKEN
```

### Execução
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar ferramenta integrada
python 07_ferramenta_integrada.py

# Ou executar scripts individuais
python 01_hello_api.py
python 02_assistente.py
# etc.
```

## Estrutura do Projeto
```
semana-04/
├── .env                    # Configurações (não versionado)
├── .gitignore             # Arquivos ignorados pelo Git
├── requirements.txt       # Dependências Python
├── 01_hello_api.py       # Consulta simples
├── 02_assistente.py      # Chatbot conversacional
├── 03_analisador.py      # Análise de texto
├── 04_tradutor.py        # Tradução
├── 05_gerador_relatorios.py  # Relatórios CSV
├── 06_teste_claude.py    # Teste Claude
├── 07_ferramenta_integrada.py  # Menu unificado
├── data/
│   ├── inputs/           # Dados de entrada
│   └── outputs/          # Resultados gerados
└── README.md             # Esta documentação
```

## Configuração

### Token GitHub
1. Acesse [GitHub Models](https://github.com/marketplace/models)
2. Gere um token de acesso
3. Adicione ao `.env`:
```
GITHUB_TOKEN=seu_token_aqui
```

### Token Claude (Opcional)
Para testar Claude:
```
ANTHROPIC_API_KEY=seu_token_claude
```

## Dados de Exemplo
- O projeto inclui um dataset CSV em `data/inputs/dados.csv`
- Use o script de download (`download_kaggle.py`) para obter novos dados

## Desenvolvimento
- Todos os scripts seguem boas práticas de Python
- Logging estruturado para debugging
- Tratamento robusto de erros
- Type hints para melhor manutenção

## Melhorias Implementadas
- Refatoração com IA para melhor robustez
- Classe de configuração centralizada
- Validação de entrada e saída
- Timeouts e rate limiting
- Interface unificada

## Contribuição
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença
Este projeto é para fins educacionais.

---

**Nota**: Este projeto utiliza APIs gratuitas do GitHub Models para evitar custos.