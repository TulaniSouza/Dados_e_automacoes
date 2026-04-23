import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constantes
DEFAULT_OUTPUT_PATH = Path("data/outputs/analise_saida.md")
PROMPT_SISTEMA = """
Você é um Analista de Dados e Segurança. Sua resposta DEVE seguir este formato:
# RELATÓRIO DE ANÁLISE
## 1. Resumo (máximo 5 linhas)
## 2. Pontos Principais
## 3. Riscos e Alertas
## 4. Ações Recomendadas
Use linguagem clara e profissional.
"""


class ConfigError(Exception):
    """Erro de configuração."""
    pass


def get_client() -> OpenAI:
    """Inicializa e retorna o cliente OpenAI com token do GitHub."""
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logging.error("GITHUB_TOKEN não encontrado no .env")
        raise ConfigError("Token de API ausente. Verifique o arquivo .env.")

    base_url = os.getenv("OPENAI_BASE_URL", "https://models.inference.ai.azure.com")
    return OpenAI(base_url=base_url, api_key=token)


def ler_entrada() -> str | None:
    """Lógica para receber texto direto ou ler de um arquivo .txt. Retorna None se falhar."""
    while True:
        print("\n--- Modo de Entrada ---")
        print("1. Digitar/Colar texto")
        print("2. Informar caminho de um arquivo .txt")

        opcao = input("\nEscolha uma opção (1 ou 2): ").strip()

        if opcao == "1":
            texto = input("Cole o texto para análise:\n> ").strip()
            if not texto:
                print("Erro: Texto não pode estar vazio.")
                continue
            return texto
        elif opcao == "2":
            caminho_str = input("Digite o caminho do arquivo (ex: dados.txt): ").strip()
            caminho = Path(caminho_str)
            if caminho.is_file():
                try:
                    return caminho.read_text(encoding="utf-8").strip()
                except IOError as e:
                    logging.error(f"Erro ao ler arquivo '{caminho}': {e}")
                    print(f"Erro: Não foi possível ler o arquivo '{caminho}'.")
                    continue
            else:
                print(f"Erro: O arquivo '{caminho}' não foi encontrado.")
                continue
        else:
            print("Opção inválida. Tente novamente.")


def analisar_com_ia(client: OpenAI, conteudo: str) -> str:
    """Envia o conteúdo para a IA com um prompt estruturado. Retorna a resposta ou mensagem de erro."""
    if not conteudo or len(conteudo) > 10000:  # Limite arbitrário para eficiência
        return "Erro: Conteúdo inválido ou muito longo."

    try:
        logging.info("Enviando texto para análise de IA")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": f"Analise o seguinte conteúdo:\n\n{conteudo}"},
            ],
            model="gpt-4o-mini",
            max_tokens=2000,  # Limite para eficiência
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        logging.error(f"Erro na API OpenAI: {e}")
        return f"Erro na API: {e}"
    except Exception as e:
        logging.exception("Erro inesperado na análise")
        return f"Erro inesperado: {e}"


def salvar_resultado(resultado: str, caminho: Path | None = None) -> None:
    """Salva o resultado em um arquivo Markdown."""
    if caminho is None:
        caminho = DEFAULT_OUTPUT_PATH
    try:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(resultado, encoding="utf-8")
        print(f"\n[Sucesso] Análise salva em '{caminho}'")
    except IOError as e:
        logging.error(f"Erro ao salvar arquivo '{caminho}': {e}")
        print(f"Erro: Não foi possível salvar em '{caminho}'.")


def main() -> None:
    try:
        client = get_client()
        print("=== Kensei Analisador Inteligente ===")

        texto_para_analisar = ler_entrada()
        if not texto_para_analisar:
            print("Nenhum texto válido fornecido. Saindo.")
            return

        resultado = analisar_com_ia(client, texto_para_analisar)

        print("\n" + "=" * 30)
        print(resultado)
        print("=" * 30)

        # Opção para caminho customizável
        salvar_opcao = input("Salvar em caminho padrão? (s/n): ").strip().lower()
        if salvar_opcao == 'n':
            caminho_str = input("Digite o caminho de saída (ex: relatorio.md): ").strip()
            salvar_resultado(resultado, Path(caminho_str))
        else:
            salvar_resultado(resultado)

    except ConfigError as e:
        print(f"Erro de configuração: {e}")
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
    except Exception as e:
        logging.exception("Erro inesperado no programa")
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()