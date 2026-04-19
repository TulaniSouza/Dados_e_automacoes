import pandas as pd
import matplotlib.pyplot as plt
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Carregar o dataset do Kaggle
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "nalisha/job-salary-prediction-dataset",
    "job_salary_prediction_dataset.csv",  # Arquivo principal do dataset
)

print("Primeiras 5 linhas do dataset:")
print(df.head())

print("\nInformações gerais do dataset:")
print(df.info())

print("\nEstatísticas descritivas:")
print(df.describe())

print("\nColunas do dataset:")
print(df.columns.tolist())

print("\nValores únicos em algumas colunas (exemplo):")
for col in df.select_dtypes(include=['object']).columns[:5]:  # Para colunas categóricas
    print(f"{col}: {df[col].unique()[:10]}")  # Mostra até 10 únicos

