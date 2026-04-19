import pandas as pd

# Carregar dados limpos
df = pd.read_csv('dados_limpos.csv')

print("Filtrando e agrupando dados...")

# Filtrar: Apenas empregos com experiência > 5 anos
df_filtrado = df[df['experience_years'] > 5]
print(f"Empregos com >5 anos de experiência: {df_filtrado.shape[0]}")

# Agrupar: Média de salário por job_title
salario_por_cargo = df_filtrado.groupby('job_title')['salary'].mean().sort_values(ascending=False)
print("\nMédia de salário por cargo (top 10):")
print(salario_por_cargo.head(10))

# Agrupar: Média de salário por industry
salario_por_industria = df_filtrado.groupby('industry')['salary'].mean().sort_values(ascending=False)
print("\nMédia de salário por indústria:")
print(salario_por_industria)

# Filtrar: Trabalhos remotos
df_remoto = df_filtrado[df_filtrado['remote_work'] == 'Yes']
print(f"\nTrabalhos remotos com >5 anos: {df_remoto.shape[0]}")

# Salvar resultados (opcional)
salario_por_cargo.to_csv('salario_por_cargo.csv')
salario_por_industria.to_csv('salario_por_industria.csv')