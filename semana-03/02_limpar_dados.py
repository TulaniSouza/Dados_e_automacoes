import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Carregar o dataset
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "nalisha/job-salary-prediction-dataset",
    "job_salary_prediction_dataset.csv",
)

print("Dados originais:")
print(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")

# Verificar valores nulos
print("\nValores nulos por coluna:")
print(df.isnull().sum())

# Remover duplicatas
df_clean = df.drop_duplicates()
print(f"\nApós remover duplicatas: {df_clean.shape[0]} linhas")

# Tratar outliers no salário (usando IQR)
Q1 = df_clean['salary'].quantile(0.25)
Q3 = df_clean['salary'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df_clean = df_clean[(df_clean['salary'] >= lower_bound) & (df_clean['salary'] <= upper_bound)]
print(f"Após remover outliers no salário: {df_clean.shape[0]} linhas")

# Salvar o dataset limpo (opcional, para usar nos próximos scripts)
df_clean.to_csv('dados_limpos.csv', index=False)
print("\nDataset limpo salvo como 'dados_limpos.csv'")