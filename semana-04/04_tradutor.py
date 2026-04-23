import logging
import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

# Configuração de constantes
logger = logging.getLogger(__name__)
DEFAULT_LANG = "Português do Brasil"
MODEL = "gpt-4o-mini"
API_BASE_URL = "https://models.inference.ai.azure.com"
OUTPUT_DIR = os.path.join("data", "outputs")
OUTPUT_FILE = "ultima_traducao.txt"


class ConfigError(Exception):
    """Erro na configuração ou carregamento de credenciais."""
    pass


class TranslationError(Exception):
    """Erro durante a tradução."""
    pass


def setup_logging(level=logging.INFO) -> None:
    """Configura o logging com formatação padrão."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def initialize_client() -> OpenAI:
    """
    Inicializa e retorna o cliente OpenAI.

    Returns:
        OpenAI: Cliente configurado

    Raises:
        ConfigError: Se GITHUB_TOKEN não for encontrado
    """
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        logger.error("GITHUB_TOKEN não encontrado em .env")
        raise ConfigError("Credencial GITHUB_TOKEN ausente")

    return OpenAI(
        base_url=API_BASE_URL,
        api_key=token,
    )


def traduzir_inteligente(client: OpenAI, texto: str, idioma_destino: str) -> str:
    """
    Traduz texto para o idioma especificado usando IA.

    Args:
        client: Cliente OpenAI configurado
        texto: Texto a traduzir
        idioma_destino: Idioma alvo da tradução

    Returns:
        str: Texto traduzido

    Raises:
        TranslationError: Se a tradução falhar
    """
    if not texto or not texto.strip():
        raise TranslationError("Texto vazio fornecido")

    if not idioma_destino or not idioma_destino.strip():
        raise TranslationError("Idioma destino inválido")

    prompt_sistema = f"""Você é um tradutor poliglota especializado em tecnologia e cibersegurança.
PASSO 1: Identifique o idioma do texto fornecido.
PASSO 2: Traduza o texto para {idioma_destino}.
PASSO 3: Mantenha termos técnicos (ex: Firewalls, Phishing, Malware) no original caso seja o padrão.
Responda APENAS com a tradução."""

    try:
        logger.info(f"Iniciando tradução para {idioma_destino}")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": texto},
            ],
            model=MODEL,
        )

        if not response.choices or not response.choices[0].message:
            raise TranslationError("Resposta inválida da API")

        result = response.choices[0].message.content
        logger.info("Tradução concluída com sucesso")
        return result

    except RateLimitError as e:
        logger.warning("Limite de taxa atingido")
        raise TranslationError("Limite de requisições atingido") from e
    except APIConnectionError as e:
        logger.error("Erro de conexão com a API")
        raise TranslationError("Falha ao conectar com a API") from e
    except APIError as e:
        logger.error(f"Erro de API: {e.status_code}")
        raise TranslationError(f"Erro da API: {e.status_code}") from e


def salvar_traducao(resultado: str, texto: str, idioma_alvo: str) -> None:
    """
    Salva o resultado da tradução em arquivo.

    Args:
        resultado: Texto traduzido
        texto: Texto original
        idioma_alvo: Idioma de destino

    Raises:
        IOError: Se houver erro ao salvar o arquivo
    """
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        caminho = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

        with open(caminho, "w", encoding="utf-8") as f:
            f.write(f"Original: {texto}\nDestino: {idioma_alvo}\nResultado: {resultado}")

        logger.info(f"Tradução salva em: {caminho}")

    except IOError as e:
        logger.error(f"Erro ao salvar tradução: {e}")
        raise


def obter_entrada_usuario(prompt: str, padrao: Optional[str] = None) -> str:
    """
    Obtém entrada do usuário com validação básica.

    Args:
        prompt: Mensagem a exibir
        padrao: Valor padrão se entrada vazia

    Returns:
        str: Entrada validada do usuário
    """
    valor = input(prompt).strip()
    return valor or padrao or ""


def main() -> None:
    """Função principal do programa."""
    setup_logging()

    try:
        logger.info("Iniciando Kensei Tradutor Universal 2.0")
        client = initialize_client()

        print("\n=== Kensei Tradutor Universal 2.0 ===")

        texto = obter_entrada_usuario("\nCole o texto (qualquer idioma): ")
        if not texto:
            logger.warning("Nenhum texto fornecido")
            print("Erro: Texto vazio fornecido.")
            return

        idioma_alvo = obter_entrada_usuario(
            "Traduzir para qual idioma? (Enter para Português): ",
            DEFAULT_LANG
        )

        resultado = traduzir_inteligente(client, texto, idioma_alvo)

        print("\n" + "=" * 50)
        print(f"Tradução ({idioma_alvo}):")
        print(resultado)
        print("=" * 50)

        salvar_traducao(resultado, texto, idioma_alvo)
        logger.info("Processo concluído com sucesso")

    except ConfigError as e:
        logger.error(f"Erro de configuração: {e}")
        print(f"Erro: {e}")
        exit(1)
    except TranslationError as e:
        logger.error(f"Erro na tradução: {e}")
        print(f"Erro durante a tradução: {e}")
        exit(1)
    except IOError as e:
        logger.error(f"Erro de I/O: {e}")
        print(f"Erro ao salvar arquivo: {e}")
        exit(1)
    except KeyboardInterrupt:
        logger.info("Programa interrompido pelo usuário")
        print("\nPrograma interrompido.")
        exit(0)
    except Exception as e:
        logger.critical(f"Erro inesperado: {e}", exc_info=True)
        print(f"Erro inesperado: {e}")
        exit(1)


if __name__ == "__main__":
    main()