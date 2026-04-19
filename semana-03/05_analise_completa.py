import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
from kagglehub import KaggleDatasetAdapter
import os

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# ETAPA 1: CARREGAR DADOS
# ============================================================================
def carregar_dados():
    """Carrega o dataset do Kaggle"""
    print("=" * 60)
    print("ETAPA 1: Carregando dados do Kaggle...")
    print("=" * 60)
    
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "nalisha/job-salary-prediction-dataset",
        "job_salary_prediction_dataset.csv",
    )
    
    print(f"✓ Dataset carregado: {df.shape[0]} linhas, {df.shape[1]} colunas")
    print(f"Colunas: {df.columns.tolist()}\n")
    
    return df


# ============================================================================
# ETAPA 2: LIMPAR DADOS
# ============================================================================
def limpar_dados(df):
    """Limpa o dataset removendo nulos, duplicatas e outliers"""
    print("=" * 60)
    print("ETAPA 2: Limpando dados...")
    print("=" * 60)
    
    print(f"Dados originais: {df.shape[0]} linhas")
    
    # Verificar valores nulos
    nulos = df.isnull().sum()
    if nulos.sum() > 0:
        print(f"Valores nulos encontrados:\n{nulos[nulos > 0]}")
        df = df.dropna()  # Remove linhas com nulos
        print(f"Após remover nulos: {df.shape[0]} linhas")
    else:
        print("✓ Nenhum valor nulo encontrado")
    
    # Remover duplicatas
    linhas_antes = df.shape[0]
    df_clean = df.drop_duplicates()
    print(f"✓ Duplicatas removidas: {linhas_antes - df_clean.shape[0]} linhas")
    
    # Tratar outliers no salário (usando IQR)
    Q1 = df_clean['salary'].quantile(0.25)
    Q3 = df_clean['salary'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    linhas_antes = df_clean.shape[0]
    df_clean = df_clean[(df_clean['salary'] >= lower_bound) & (df_clean['salary'] <= upper_bound)]
    print(f"✓ Outliers removidos: {linhas_antes - df_clean.shape[0]} linhas")
    print(f"✓ Dados finais: {df_clean.shape[0]} linhas\n")
    
    return df_clean


# ============================================================================
# ETAPA 3: FILTRAR E AGRUPAR
# ============================================================================
def filtrar_agrupar(df):
    """Filtra e agrupa dados por cargo e indústria"""
    print("=" * 60)
    print("ETAPA 3: Filtrando e agrupando dados...")
    print("=" * 60)
    
    # Filtrar: Apenas empregos com experiência > 5 anos
    df_filtrado = df[df['experience_years'] > 5]
    print(f"✓ Empregos com >5 anos de experiência: {df_filtrado.shape[0]} linhas")
    
    # Agrupar: Média de salário por job_title
    salario_por_cargo = df_filtrado.groupby('job_title')['salary'].mean().sort_values(ascending=False)
    print(f"\n📊 Média de salário por cargo (Top 10):")
    print(salario_por_cargo.head(10))
    
    # Agrupar: Média de salário por industry
    salario_por_industria = df_filtrado.groupby('industry')['salary'].mean().sort_values(ascending=False)
    print(f"\n📊 Média de salário por indústria:")
    print(salario_por_industria)
    
    # Filtrar: Trabalhos remotos
    df_remoto = df_filtrado[df_filtrado['remote_work'] == 'Yes']
    print(f"\n✓ Trabalhos remotos com >5 anos: {df_remoto.shape[0]} linhas\n")
    
    return df_filtrado, salario_por_cargo, salario_por_industria


# ============================================================================
# ETAPA 4: GERAR GRÁFICOS
# ============================================================================
def gerar_graficos(df, salario_por_cargo, salario_por_industria):
    """Gera e salva todos os gráficos na pasta 'graficos'"""
    print("=" * 60)
    print("ETAPA 4: Gerando gráficos...")
    print("=" * 60)
    
    # Criar pasta graficos se não existir
    os.makedirs('graficos', exist_ok=True)
    
    # GRÁFICO 1: Histograma de salários
    print("Gerando: Histograma de salários...")
    plt.figure(figsize=(10, 6))
    plt.hist(df['salary'], bins=50, color='#2E86AB', alpha=0.7, edgecolor='black')
    plt.title('Distribuição de Salários', fontsize=14, fontweight='bold')
    plt.xlabel('Salário (R$)', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('graficos/01_histograma_salarios.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Salvo: graficos/01_histograma_salarios.png")
    
    # GRÁFICO 2: Boxplot de salários por indústria
    print("Gerando: Boxplot por indústria...")
    plt.figure(figsize=(14, 7))
    sns.boxplot(x='industry', y='salary', data=df, palette='Set2')
    plt.title('Distribuição de Salários por Indústria', fontsize=14, fontweight='bold')
    plt.xlabel('Indústria', fontsize=12)
    plt.ylabel('Salário (R$)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('graficos/02_boxplot_industria.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Salvo: graficos/02_boxplot_industria.png")
    
    # GRÁFICO 3: Scatter plot experiência vs salário
    print("Gerando: Scatter plot (Experiência vs Salário)...")
    plt.figure(figsize=(10, 6))
    plt.scatter(df['experience_years'], df['salary'], alpha=0.5, color='#A23B72', s=50)
    plt.title('Relação entre Experiência e Salário', fontsize=14, fontweight='bold')
    plt.xlabel('Anos de Experiência', fontsize=12)
    plt.ylabel('Salário (R$)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('graficos/03_scatter_experiencia_salario.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Salvo: graficos/03_scatter_experiencia_salario.png")
    
    # GRÁFICO 4: Barplot média salário por cargo (top 10)
    print("Gerando: Barplot de salário por cargo...")
    plt.figure(figsize=(12, 7))
    colors = plt.cm.viridis(salario_por_cargo.head(10).values / salario_por_cargo.head(10).max())
    plt.barh(range(len(salario_por_cargo.head(10))), salario_por_cargo.head(10).values, color=colors)
    plt.yticks(range(len(salario_por_cargo.head(10))), salario_por_cargo.head(10).index)
    plt.xlabel('Salário Médio (R$)', fontsize=12)
    plt.title('Média de Salário por Cargo (Top 10)', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')
    # Adicionar valores nas barras
    for i, (idx, val) in enumerate(salario_por_cargo.head(10).items()):
        plt.text(val, i, f' R${val:,.0f}', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig('graficos/04_barplot_cargo_top10.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Salvo: graficos/04_barplot_cargo_top10.png")
    
    # GRÁFICO 5: Barplot média salário por indústria
    print("Gerando: Barplot de salário por indústria...")
    plt.figure(figsize=(14, 8))
    colors = plt.cm.Blues(salario_por_industria.values / salario_por_industria.max())
    plt.barh(range(len(salario_por_industria)), salario_por_industria.values, color=colors)
    plt.yticks(range(len(salario_por_industria)), salario_por_industria.index)
    plt.xlabel('Salário Médio (R$)', fontsize=12)
    plt.title('Média de Salário por Indústria', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')
    # Adicionar valores nas barras
    for i, (idx, val) in enumerate(salario_por_industria.items()):
        plt.text(val, i, f' R${val:,.0f}', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig('graficos/05_barplot_industria.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Salvo: graficos/05_barplot_industria.png")
    
    print(f"\n✓ Todos os gráficos salvos na pasta 'graficos/'!\n")


# ============================================================================
# FLUXO PRINCIPAL
# ============================================================================
def main():
    """Executa todo o fluxo de análise"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  ANÁLISE COMPLETA - Predição de Salários em Empregos   ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # Executar o fluxo
        df = carregar_dados()
        df_clean = limpar_dados(df)
        df_filtrado, salario_cargo, salario_industria = filtrar_agrupar(df_clean)
        gerar_graficos(df_clean, salario_cargo, salario_industria)
        
        # Resumo final
        print("=" * 60)
        print("RESUMO DA ANÁLISE")
        print("=" * 60)
        print(f"✓ Total de registros processados: {df_clean.shape[0]:,}")
        print(f"✓ Gráficos gerados: 5")
        print(f"✓ Pasta de saída: ./graficos/")
        print("\n✅ Análise completa realizada com sucesso!\n")
        
    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}\n")
        raise


if __name__ == "__main__":
    main()
