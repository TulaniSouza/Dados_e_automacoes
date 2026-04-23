import logging
import os
from collections import deque
from typing import Optional
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI, APIError, APITimeoutError, RateLimitError

# ============================================================================
# CONFIGURAÇÃO E CONSTANTES
# ============================================================================

@dataclass
class AssistantConfig:
    """Configuração centralizada do assistente."""
    max_history_size: int = 10
    model: str = "gpt-4o-mini"
    api_timeout: float = 30.0
    base_url: str = "https://models.inference.ai.azure.com"

    @classmethod
    def from_env(cls) -> "AssistantConfig":
        """Carrega configuração de variáveis de ambiente."""
        return cls(
            max_history_size=int(os.getenv("MAX_HISTORY", 10)),
            model=os.getenv("MODEL", "gpt-4o-mini"),
            api_timeout=float(os.getenv("API_TIMEOUT", 30.0))
        )


# ============================================================================
# LOGGING
# ============================================================================

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Configura logging estruturado."""
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    return logger


logger = setup_logging()


# ============================================================================
# CLIENTE E HISTÓRICO
# ============================================================================

class ConversationHistory:
    """Gerencia histórico de conversa com limite de tamanho."""

    def __init__(self, max_size: int = 10):
        self.system_message = {
            "role": "system",
            "content": "Você é um especialista em cibersegurança. Responda em pt-BR de forma clara e concisa."
        }
        self.max_size = max_size
        self.messages: deque = deque([self.system_message], maxlen=max_size + 1)

    def add_user_message(self, content: str) -> None:
        """Adiciona mensagem do usuário."""
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        """Adiciona mensagem do assistente."""
        self.messages.append({"role": "assistant", "content": content})

    def get_all(self) -> list[dict]:
        """Retorna todas as mensagens (incluindo sistema)."""
        return list(self.messages)

    def clear(self) -> None:
        """Reseta o histórico."""
        self.messages.clear()
        self.messages.append(self.system_message)


def get_client(config: AssistantConfig) -> OpenAI:
    """
    Inicializa cliente OpenAI com validação.

    Raises:
        EnvironmentError: Se a chave de API não estiver configurada.
    """
    load_dotenv()
    api_key = os.getenv("GITHUB_TOKEN")

    if not api_key:
        logger.error("GITHUB_TOKEN não encontrado no .env")
        raise EnvironmentError("GITHUB_TOKEN é obrigatório. Configure em .env")

    logger.info(f"Cliente OpenAI inicializado para {config.model}")
    return OpenAI(
        base_url=config.base_url,
        api_key=api_key,
        timeout=config.api_timeout,
    )


# ============================================================================
# PROCESSAMENTO DE CONVERSA
# ============================================================================

def get_assistant_response(
    client: OpenAI,
    history: ConversationHistory,
    config: AssistantConfig
) -> Optional[str]:
    """
    Obtém resposta do assistente com tratamento robusto de erros.

    Returns:
        Conteúdo da resposta ou None se falhar.
    """
    try:
        response = client.chat.completions.create(
            messages=history.get_all(),
            model=config.model,
        )

        # Validação da resposta
        if not response.choices or not response.choices[0].message.content:
            logger.warning("Resposta vazia recebida da API")
            return None

        content = response.choices[0].message.content.strip()
        logger.debug(f"Resposta recebida: {len(content)} caracteres")
        return content

    except RateLimitError:
        logger.error("Limite de taxa atingido. Aguarde antes de tentar novamente.")
        return None
    except APITimeoutError:
        logger.error("Timeout na requisição à API (timeout: {config.api_timeout}s)")
        return None
    except APIError as e:
        logger.error(f"Erro de API: {e.status_code} - {e.message}")
        return None
    except Exception as e:
        logger.exception(f"Erro inesperado ao chamar API: {type(e).__name__}")
        return None


def run_assistant(config: Optional[AssistantConfig] = None) -> int:
    """
    Loop principal do assistente.

    Args:
        config: Configuração do assistente (usa defaults se None)

    Returns:
        Código de saída (0 = sucesso, 1 = erro)
    """
    config = config or AssistantConfig.from_env()

    try:
        client = get_client(config)
    except EnvironmentError as e:
        logger.critical(f"Falha ao inicializar: {e}")
        return 1

    history = ConversationHistory(max_size=config.max_history_size)

    print("\n" + "="*60)
    print("🔐 Assistente Kensei - Especialista em Cibersegurança")
    print("="*60)
    print("Comandos: 'sair' ou 'exit' para encerrar, Ctrl+C para interromper")
    print("="*60 + "\n")

    logger.info("Sessão iniciada")

    try:
        while True:
            try:
                user_input = input("\n👤 Você: ").strip()
            except EOFError:
                logger.info("Sessão encerrada por EOF")
                print("\n👋 Encerrando por EOF.")
                break
            except KeyboardInterrupt:
                logger.info("Sessão interrompida por usuário (Ctrl+C)")
                raise

            # Validação de entrada
            if not user_input:
                continue

            if user_input.lower() in ["sair", "exit"]:
                logger.info("Sessão encerrada por comando do usuário")
                print("\n👋 Até mais! Sessão encerrada.")
                break

            if len(user_input) > 5000:
                print("⚠️  Entrada muito longa (máx: 5000 caracteres). Tente novamente.")
                logger.warning(f"Entrada rejeitada por ser muito longa: {len(user_input)} chars")
                continue

            # Adiciona mensagem ao histórico
            history.add_user_message(user_input)
            logger.debug(f"Mensagem do usuário adicionada ao histórico")

            # Obtém resposta
            print("\n🤔 Assistente pensando...", end="\r", flush=True)
            response = get_assistant_response(client, history, config)

            if response is None:
                print(" " * 50, end="\r")
                print("❌ Falha ao processar. Tente novamente ou use 'sair' para encerrar.")
                logger.warning("Resposta da API foi None")
                continue

            print(" " * 50, end="\r")
            print(f"🤖 Assistente: {response}\n")
            history.add_assistant_message(response)
            logger.info("Resposta do assistente enviada ao usuário")

    except KeyboardInterrupt:
        logger.info("Interrupção por Ctrl+C")
        print("\n\n👋 Sessão interrompida. Até mais!")
    except Exception as e:
        logger.exception(f"Erro crítico: {type(e).__name__}: {e}")
        return 1

    logger.info("Sessão finalizada com sucesso")
    return 0


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    exit_code = run_assistant()
    exit(exit_code)
