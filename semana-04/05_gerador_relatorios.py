"""
Módulo de geração de relatórios executivos usando IA.
"""

import logging
import os
from pathlib import Path
from typing import Optional

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constantes
GITHUB_TOKEN_ENV = "GITHUB_TOKEN"
API_BASE_URL = "https://models.inference.ai.azure.com"
API_MODEL = "gpt-4o-mini"
API_TIMEOUT = 60  # segundos
SYSTEM_PROMPT = "Você é um gestor de TI e especialista em dados."

# Caminhos
DATA_DIR = Path("data")
INPUT_DIR = DATA_DIR / "inputs"
OUTPUT_DIR = DATA_DIR / "outputs"
CSV_FILE = INPUT_DIR / "dados.csv"
OUTPUT_FILE = OUTPUT_DIR / "relatorio_final.md"

# ============================================================================
# EXCEÇÕES CUSTOMIZADAS
# ============================================================================


class ReportGeneratorError(Exception):
    """Exceção base para erros do gerador de relatórios."""
    pass


class ConfigurationError(ReportGeneratorError):
    """Erro de configuração (credenciais, variáveis de ambiente)."""
    pass


class DataValidationError(ReportGeneratorError):
    """Erro na validação dos dados."""
    pass


class APIError(ReportGeneratorError):
    """Erro ao comunicar com a API."""
    pass


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================


def get_client() -> OpenAI:
    """
    Obtém cliente OpenAI configurado com credenciais do ambiente.

    Raises:
        ConfigurationError: Se GITHUB_TOKEN não estiver definido.

    Returns:
        OpenAI: Cliente OpenAI configurado.
    """
    load_dotenv()
    token = os.getenv(GITHUB_TOKEN_ENV)

    if not token:
        msg = f"{GITHUB_TOKEN_ENV} não encontrado no .env"
        logger.error(msg)
        raise ConfigurationError(msg)

    return OpenAI(
        base_url=API_BASE_URL,
        api_key=token,
    )


def load_csv_data(file_path: Path) -> pd.DataFrame:
    """
    Carrega dados de arquivo CSV com validação.

    Args:
        file_path: Caminho do arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame carregado.

    Raises:
        DataValidationError: Se arquivo não existe ou está vazio.
    """
    if not file_path.exists():
        msg = f"Arquivo não encontrado: {file_path}"
        logger.error(msg)
        raise DataValidationError(msg)

    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        logger.warning("Erro com encoding UTF-8, tentando latin-1...")
        df = pd.read_csv(file_path, encoding="latin-1")
    except Exception as e:
        msg = f"Erro ao ler CSV: {e}"
        logger.error(msg)
        raise DataValidationError(msg) from e

    if df.empty:
        msg = "CSV não contém dados"
        logger.error(msg)
        raise DataValidationError(msg)

    logger.info(f"Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
    return df


def validate_dataframe(df: pd.DataFrame) -> None:
    """
    Valida integridade do DataFrame.

    Args:
        df: DataFrame a validar.

    Raises:
        DataValidationError: Se validação falhar.
    """
    if df.shape[0] == 0:
        raise DataValidationError("DataFrame vazio")

    if df.shape[1] == 0:
        raise DataValidationError("DataFrame sem colunas")


def generate_data_summary(df: pd.DataFrame) -> dict:
    """
    Gera resumo estatístico dos dados.

    Args:
        df: DataFrame para análise.

    Returns:
        dict: Resumo com estatísticas.
    """
    return {
        "total_records": len(df),
        "columns": ", ".join(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "missing_percentage": round((df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2),
        "statistical_summary": df.describe(include="all").to_string(),
    }


def build_report_prompt(data_summary: dict) -> str:
    """
    Constrói prompt para a IA gerar relatório.

    Args:
        data_summary: Dicionário com resumo dos dados.

    Returns:
        str: Prompt formatado.
    """
    return f"""
Analise os seguintes dados extraídos de um arquivo CSV:
- Total de registros: {data_summary['total_records']}
- Colunas identificadas: {data_summary['columns']}
- Total de valores ausentes: {data_summary['missing_values']} ({data_summary['missing_percentage']}%)

Resumo dos dados:
{data_summary['statistical_summary']}

Gere um relatório executivo em Markdown com:
1. Resumo Executivo (o que esses dados representam)
2. Achados principais (tendências e padrões)
3. Riscos/Anomalias detectadas
4. Ações recomendadas para o time técnico.
"""


def call_api_for_report(client: OpenAI, prompt: str) -> str:
    """
    Chama API para gerar relatório.

    Args:
        client: Cliente OpenAI.
        prompt: Prompt para a IA.

    Returns:
        str: Conteúdo do relatório.

    Raises:
        APIError: Se falhar a comunicação com a API.
    """
    try:
        logger.info("Chamando API para gerar relatório...")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            model=API_MODEL,
            timeout=API_TIMEOUT,
        )

        if not response.choices or not response.choices[0].message:
            raise APIError("Resposta vazia da API")

        report = response.choices[0].message.content

        if not report or not isinstance(report, str):
            raise APIError("Conteúdo de relatório inválido")

        logger.info("Relatório gerado com sucesso")
        return report

    except APITimeoutError as e:
        msg = f"Timeout na chamada da API: {e}"
        logger.error(msg)
        raise APIError(msg) from e
    except APIConnectionError as e:
        msg = f"Erro de conexão com API: {e}"
        logger.error(msg)
        raise APIError(msg) from e
    except Exception as e:
        msg = f"Erro inesperado na API: {e}"
        logger.error(msg)
        raise APIError(msg) from e


def save_report(content: str, file_path: Path) -> None:
    """
    Salva relatório em arquivo.

    Args:
        content: Conteúdo do relatório.
        file_path: Caminho para salvar.

    Raises:
        IOError: Se falhar ao salvar.
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        logger.info(f"Relatório salvo: {file_path}")
    except IOError as e:
        msg = f"Erro ao salvar arquivo: {e}"
        logger.error(msg)
        raise IOError(msg) from e


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================


def gerar_relatorio() -> None:
    """
    Orquestra todo o processo de geração de relatório.
    """
    print("=== Kensei Gerador de Relatórios Executivos ===\n")

    try:
        # 1. Carrega cliente e dados
        logger.info("Inicializando...")
        client = get_client()
        df = load_csv_data(CSV_FILE)

        # 2. Valida dados
        validate_dataframe(df)

        # 3. Gera resumo
        logger.info("Processando dados...")
        data_summary = generate_data_summary(df)

        # 4. Constrói prompt e chama API
        prompt = build_report_prompt(data_summary)
        report_content = call_api_for_report(client, prompt)

        # 5. Salva relatório
        save_report(report_content, OUTPUT_FILE)

        print("\n" + "=" * 50)
        print("✓ Relatório gerado com sucesso!")
        print(f"✓ Arquivo salvo: {OUTPUT_FILE}")
        print("=" * 50)

    except ConfigurationError as e:
        logger.critical(f"Erro de configuração: {e}")
        print(f"\n❌ Erro de configuração: {e}")
        raise SystemExit(1)
    except DataValidationError as e:
        logger.error(f"Erro na validação de dados: {e}")
        print(f"\n❌ Erro nos dados: {e}")
        raise SystemExit(1)
    except APIError as e:
        logger.error(f"Erro na API: {e}")
        print(f"\n❌ Erro ao gerar relatório: {e}")
        raise SystemExit(1)
    except Exception as e:
        logger.exception("Erro não esperado")
        print(f"\n❌ Erro inesperado: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    gerar_relatorio()
