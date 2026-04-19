import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# Criar pasta graficos se não existir
os.makedirs('graficos', exist_ok=True)

# Carregar dados limpos
df = pd.read_csv('dados_limpos.csv')

# Gráfico 1: Histograma de salários com matplotlib
plt.figure(figsize=(10, 6))
plt.hist(df['salary'], bins=50, color='blue', alpha=0.7)
plt.title('Distribuição de Salários')
plt.xlabel('Salário')
plt.ylabel('Frequência')
plt.savefig('graficos/histograma_salarios.png')
plt.show()

# Gráfico 2: Boxplot de salários por indústria com seaborn
plt.figure(figsize=(12, 8))
sns.boxplot(x='industry', y='salary', data=df)
plt.title('Salários por Indústria')
plt.xticks(rotation=45)
plt.savefig('graficos/boxplot_industria.png')
plt.show()

# Gráfico 3: Scatter plot experiência vs salário com matplotlib
plt.figure(figsize=(10, 6))
plt.scatter(df['experience_years'], df['salary'], alpha=0.5)
plt.title('Experiência vs Salário')
plt.xlabel('Anos de Experiência')
plt.ylabel('Salário')
plt.savefig('graficos/scatter_experiencia_salario.png')
plt.show()

# Gráfico 4: Gráfico de barras média salário por cargo (top 10) com plotly (experimental)
salario_por_cargo = df.groupby('job_title')['salary'].mean().sort_values(ascending=False).head(10)
fig = px.bar(salario_por_cargo, x=salario_por_cargo.index, y=salario_por_cargo.values,
             title='Média de Salário por Cargo (Top 10)', labels={'y':'Salário Médio', 'x':'Cargo'})
fig.write_image('graficos/barplot_cargo.png')
# fig.show()  # Para interativo, mas salvamos como PNG

print("Gráficos salvos na pasta 'graficos/'")