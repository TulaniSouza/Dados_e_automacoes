"""
Módulo de interação com a API GitHub Models.

Este módulo fornece uma interface simples para comunicar com modelos de IA
hospedados no GitHub Models usando a API OpenAI-compatible.
"""

import logging
import os
import sys
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError


# Configurar logging profissional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_configuration() -> str:
    """
    Carrega e valida as configurações de token da API.

    Returns:
        str: O token da API

    Raises:
        SystemExit: Se o token não for encontrado
    """
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        logger.error("GITHUB_TOKEN não encontrado no arquivo .env")
        sys.exit(1)

    if not token.strip():
        logger.error("GITHUB_TOKEN está vazio")
        sys.exit(1)

    logger.info("Configuração carregada com sucesso")
    return token


def initialize_client(token: str) -> OpenAI:
    """
    Inicializa o cliente OpenAI para GitHub Models.

    Args:
        token: Token de autenticação da API

    Returns:
        OpenAI: Cliente configurado
    """
    return OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=token,
        timeout=30.0,  # Timeout de 30 segundos
    )


def get_user_input() -> str:
    """
    Obtém e valida a entrada do usuário.

    Returns:
        str: A pergunta do usuário

    Raises:
        SystemExit: Se o usuário não fornecer entrada válida
    """
    try:
        pergunta = input("\nDigite sua pergunta: ").strip()

        if not pergunta:
            logger.error("A pergunta não pode estar vazia")
            sys.exit(1)

        if len(pergunta) > 5000:
            logger.error("A pergunta é muito longa (máximo 5000 caracteres)")
            sys.exit(1)

        return pergunta
    except KeyboardInterrupt:
        logger.info("Execução cancelada pelo usuário")
        sys.exit(0)


def query_ai(client: OpenAI, pergunta: str) -> Optional[str]:
    """
    Envia uma pergunta para o modelo de IA e retorna a resposta.

    Args:
        client: Cliente OpenAI configurado
        pergunta: Pergunta para enviar

    Returns:
        str: Resposta da IA, ou None se ocorrer erro
    """
    try:
        logger.info("Consultando a IA no GitHub Models...")

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": pergunta}],
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=1000,
        )

        # Validar que temos uma resposta
        if not response.choices or len(response.choices) == 0:
            logger.error("Resposta vazia do servidor")
            return None

        conteudo = response.choices[0].message.content

        if not conteudo:
            logger.warning("Conteúdo da resposta está vazio")
            return None

        logger.info("Resposta recebida com sucesso")
        return conteudo

    except APITimeoutError:
        logger.error("Timeout: A requisição demorou muito tempo")
        return None
    except APIConnectionError:
        logger.error("Erro de conexão: Verifique sua conexão com a internet e o endpoint da API")
        return None
    except APIError as e:
        logger.error(f"Erro da API: {e.message}")
        if e.status_code == 401:
            logger.error("Token inválido ou expirado")
        elif e.status_code == 429:
            logger.error("Limite de requisições atingido - tente novamente mais tarde")
        elif e.status_code == 404:
            logger.error("Modelo não encontrado")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado: {type(e).__name__}: {e}")
        return None


def main() -> None:
    """Função principal."""
    try:
        # Carregar configuração
        token = load_configuration()

        # Inicializar cliente
        client = initialize_client(token)

        # Obter entrada do usuário
        pergunta = get_user_input()

        # Consultar IA
        resposta = query_ai(client, pergunta)

        # Exibir resultado
        if resposta:
            print("\n" + "="*50)
            print("--- RESPOSTA ---")
            print("="*50)
            print(resposta)
            print("="*50)
        else:
            logger.error("Não foi possível obter uma resposta válida")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("\nPrograma interrompido pelo usuário")
        sys.exit(0)


if __name__ == "__main__":
    main()