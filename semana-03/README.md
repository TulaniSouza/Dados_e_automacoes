# Análise de Previsão de Salários em Empregos

Projeto de análise de dados que consolida um fluxo completo de processamento: carregamento, limpeza, transformação e visualização de dados de salários em diferentes cargos e indústrias.

## Objetivo

Analisar um dataset de 250.000 registros de empregos para identificar padrões de salários por cargo, indústria, experiência e modalidade de trabalho (remoto/presencial).

## Estrutura do Projeto

```
semana-03/
├── 01_explorar_dados.py          # Exploração inicial dos dados
├── 02_limpar_dados.py            # Limpeza e tratamento de outliers
├── 03_filtrar_agrupar.py         # Filtragem e agregação de dados
├── 04_graficos.py                # Geração individual de gráficos
├── 05_analise_completa.py        #  Script unificado (RECOMENDADO)
├── graficos/                     # Pasta com gráficos em PNG (gerados)
├── dados_limpos.csv              # Dataset limpo (gerado)
├── salario_por_cargo.csv         # Aggregações por cargo (gerado)
├── salario_por_industria.csv     # Aggregações por indústria (gerado)
├── .gitignore                    # Arquivos a ignorar no Git
└── README.md                     # Este arquivo
```

## Como Usar

### Pré-requisitos

- Python 3.8+
- pip ou conda

### Instalação

1. **Clone o repositório:**
```bash
git clone <seu-repositorio>
cd semana-03
```

2. **Crie um ambiente virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

### Executar a Análise

**Opção 1 - RECOMENDADO (Fluxo Completo):**
```bash
python 05_analise_completa.py
```
Isso executa todo o pipeline em um único comando:
- ✅ Carrega dados do Kaggle
- ✅ Limpa e trata outliers
- ✅ Filtra e agrupa por cargo/indústria
- ✅ Gera 5 gráficos em alta resolução (300 DPI)

**Opção 2 - Scripts Individuais (Estudo/Debug):**
```bash
python 01_explorar_dados.py      # Exploração inicial
python 02_limpar_dados.py        # Limpeza
python 03_filtrar_agrupar.py     # Agregações
python 04_graficos.py            # Gráficos (opcional)
```

## Gráficos Gerados

Após executar `05_analise_completa.py`, você encontrará na pasta `graficos/`:

| Arquivo | Descrição |
|---------|-----------|
| `01_histograma_salarios.png` | Distribuição de salários |
| `02_boxplot_industria.png` | Salários por indústria (boxplot) |
| `03_scatter_experiencia_salario.png` | Relação experiência vs salário |
| `04_barplot_cargo_top10.png` | Top 10 cargos com maior salário |
| `05_barplot_industria.png` | Salários médios por indústria |

## Resultados Principais

**Dataset Processado:**
- 📌 Total de registros: 247.664 (após limpeza)
- 📌 Outliers removidos: 2.336
- 📌 Registros com >5 anos de experiência: 176.192
- 📌 Trabalhos remotos: 58.087

**Top 5 Cargos Melhor Pagos:**
1. AI Engineer - R$ 176.948
2. Machine Learning Engineer - R$ 168.804
3. Product Manager - R$ 163.680
4. Cloud Engineer - R$ 158.911
5. DevOps Engineer - R$ 157.012

**Indústrias com Melhor Remuneração:**
1. Technology - R$ 152.731
2. Education - R$ 152.714
3. Finance - R$ 152.610

## Tecnologias Utilizadas

- **Pandas** - Manipulação de dados
- **Matplotlib & Seaborn** - Visualizações estáticas
- **Kagglehub** - Acesso ao dataset
- **Python 3.12** - Linguagem base

## 📝 Lógica do Pipeline

```
┌─────────────────────────┐
│ 1. CARREGAR DADOS       │ (Kaggle - 250k registros)
└────────────┬────────────┘
             │
┌────────────▼────────────┐
│ 2. LIMPAR DADOS         │ (Remove nulos, duplicatas, outliers)
└────────────┬────────────┘
             │
┌────────────▼────────────┐
│ 3. FILTRAR & AGRUPAR    │ (>5 anos experiência, por cargo/indústria)
└────────────┬────────────┘
             │
┌────────────▼────────────┐
│ 4. GERAR GRÁFICOS       │ (5 visualizações em 300 DPI)
└────────────┬────────────┘
             │
         PRONTO! ✅
```

## Insights Obtidos

1. **Cargos de TI/IA** ganham significativamente mais (>R$ 150k)
2. **Experiência importa**: >5 anos impacta nos salários
3. **Trabalho remoto** é comum (33% dos registros com >5 anos)
4. **Indústria** tem pouco impacto (variação <1% entre elas)

## Tratamento de Dados

- **Valores nulos**: Removidos
- **Duplicatas**: Removidas
- **Outliers**: IQR (Interquartile Range) method
  - Limite inferior: Q1 - 1.5×IQR
  - Limite superior: Q3 + 1.5×IQR

## Troubleshooting

**Erro: ModuleNotFoundError (pandas, matplotlib, etc)**
```bash
pip install pandas matplotlib seaborn kagglehub plotly
```

**Erro: Kaggle authentication**
- Certifique-se que tem credenciais Kaggle configuradas
- Veja: https://www.kaggle.com/settings/account

**Gráficos não salvam**
- Verifique se tem permissão de escrita na pasta `graficos/`
- A pasta é criada automaticamente, mas precisa de espaço em disco

## Arquivo de Dependências

Crie um arquivo `requirements.txt` com:

```
pandas==2.0.3
matplotlib==3.7.2
seaborn==0.12.2
kagglehub==0.2.13
plotly==5.17.0
```

Instale com:
```bash
pip install -r requirements.txt
```

## Autor

Desenvolvido como projeto de análise de dados - Semana 03

## Licença

Livre para uso pessoal e educacional.

## Contribuições

Para contribuir:
1. Faça um Fork
2. Crie uma branch (`git checkout -b feature/melhorias`)
3. Commit suas mudanças (`git commit -m 'Adiciona X'`)
4. Push para a branch (`git push origin feature/melhorias`)
5. Abra um Pull Request

---

**Última atualização:** 19 de abril de 2026
