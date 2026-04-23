"""
Ferramenta Integrada de Automação com IA

Esta ferramenta combina múltiplas funcionalidades de IA em um único script:
- Consulta simples à IA
- Assistente conversacional
- Análise de texto
- Tradução de idiomas
- Geração de relatórios a partir de CSV
- Teste da API Claude (opcional)

Uso: python 07_ferramenta_integrada.py
"""

import os
import sys
import logging
from typing import Dict, Callable
from dotenv import load_dotenv
from openai import OpenAI

# Carregar configurações
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FerramentaIntegrada:
    """Classe principal que integra todas as funcionalidades."""

    def __init__(self):
        self.client = self._inicializar_cliente()
        self.funcoes: Dict[str, Callable] = {
            "1": self.consulta_simples,
            "2": self.assistente_conversacional,
            "3": self.analisador_texto,
            "4": self.tradutor,
            "5": self.gerador_relatorios,
            "6": self.teste_claude,
            "0": self.sair
        }

    def _inicializar_cliente(self) -> OpenAI:
        """Inicializa cliente OpenAI."""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            logger.error("GITHUB_TOKEN não encontrado")
            sys.exit(1)

        return OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=token,
            timeout=30.0
        )

    def mostrar_menu(self) -> None:
        """Exibe o menu principal."""
        print("\n" + "="*60)
        print("🛠️  FERRAMENTA INTEGRADA DE AUTOMAÇÃO COM IA")
        print("="*60)
        print("1. Consulta Simples à IA")
        print("2. Assistente Conversacional")
        print("3. Analisador de Texto")
        print("4. Tradutor de Idiomas")
        print("5. Gerador de Relatórios (CSV)")
        print("6. Teste API Claude")
        print("0. Sair")
        print("="*60)

    def consulta_simples(self) -> None:
        """Executa consulta simples (similar ao 01_hello_api.py)."""
        print("\n--- CONSULTA SIMPLES ---")
        pergunta = input("Digite sua pergunta: ").strip()
        if not pergunta:
            return

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": pergunta}],
                model="gpt-4o-mini",
                temperature=0.7,
                max_tokens=1000
            )
            print(f"\nResposta: {response.choices[0].message.content}")
        except Exception as e:
            logger.error(f"Erro na consulta: {e}")

    def assistente_conversacional(self) -> None:
        """Executa assistente conversacional (similar ao 02_assistente.py)."""
        print("\n--- ASSISTENTE CONVERSACIONAL ---")
        print("Digite 'sair' para voltar ao menu principal")

        historico = [{
            "role": "system",
            "content": "Você é um assistente útil. Responda em português."
        }]

        while True:
            entrada = input("\nVocê: ").strip()
            if entrada.lower() in ["sair", "exit"]:
                break

            if not entrada:
                continue

            historico.append({"role": "user", "content": entrada})

            try:
                response = self.client.chat.completions.create(
                    messages=historico,
                    model="gpt-4o-mini"
                )
                resposta = response.choices[0].message.content
                print(f"Assistente: {resposta}")
                historico.append({"role": "assistant", "content": resposta})
            except Exception as e:
                logger.error(f"Erro no assistente: {e}")

    def analisador_texto(self) -> None:
        """Executa análise de texto (similar ao 03_analisador.py)."""
        print("\n--- ANALISADOR DE TEXTO ---")
        texto = input("Digite o texto para analisar: ").strip()
        if not texto:
            return

        prompt = f"""
        Analise o seguinte texto e forneça:
        1. Resumo executivo
        2. Principais temas
        3. Sentimento geral
        4. Sugestões de melhoria

        Texto: {texto}
        """

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini",
                temperature=0.5,
                max_tokens=1500
            )
            print(f"\nAnálise: {response.choices[0].message.content}")
        except Exception as e:
            logger.error(f"Erro na análise: {e}")

    def tradutor(self) -> None:
        """Executa tradução (similar ao 04_tradutor.py)."""
        print("\n--- TRADUTOR ---")
        texto = input("Digite o texto para traduzir: ").strip()
        idioma = input("Para qual idioma? (ex: inglês, espanhol, francês): ").strip()

        if not texto or not idioma:
            return

        prompt = f"Traduza o seguinte texto para {idioma}: {texto}"

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini",
                temperature=0.3
            )
            print(f"\nTradução: {response.choices[0].message.content}")
        except Exception as e:
            logger.error(f"Erro na tradução: {e}")

    def gerador_relatorios(self) -> None:
        """Executa geração de relatórios (similar ao 05_gerador_relatorios.py)."""
        print("\n--- GERADOR DE RELATÓRIOS ---")
        csv_path = "data/inputs/dados.csv"

        if not os.path.exists(csv_path):
            print(f"Arquivo CSV não encontrado: {csv_path}")
            return

        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            stats = df.describe().to_string()

            prompt = f"""
            Com base nas seguintes estatísticas do dataset CSV:

            {stats}

            Gere um relatório executivo profissional em Markdown com:
            - Introdução aos dados
            - Análise estatística
            - Insights principais
            - Conclusões
            """

            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-4o-mini",
                temperature=0.5,
                max_tokens=2000
            )

            relatorio = response.choices[0].message.content
            print(f"\nRelatório gerado:\n{relatorio}")

            # Salvar relatório
            output_path = "data/outputs/relatorio_integrado.md"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(relatorio)
            print(f"\nRelatório salvo em: {output_path}")

        except Exception as e:
            logger.error(f"Erro no gerador de relatórios: {e}")

    def teste_claude(self) -> None:
        """Testa API do Claude (similar ao 06_teste_claude.py)."""
        print("\n--- TESTE API CLAUDE ---")
        try:
            from anthropic import Anthropic

            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key or api_key == "YOUR_ANTHROPIC_API_KEY":
                print("Chave ANTHROPIC_API_KEY não configurada no .env")
                return

            client = Anthropic(api_key=api_key)
            query = input("Digite sua consulta para Claude: ").strip()

            if not query:
                return

            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.7,
                system="Você é um assistente útil.",
                messages=[{"role": "user", "content": query}]
            )

            print(f"\nResposta do Claude: {message.content[0].text}")

        except ImportError:
            print("Biblioteca anthropic não instalada. Instale com: pip install anthropic")
        except Exception as e:
            logger.error(f"Erro no teste Claude: {e}")

    def sair(self) -> None:
        """Sai da ferramenta."""
        print("\n👋 Até mais!")
        sys.exit(0)

    def executar(self) -> None:
        """Loop principal da ferramenta."""
        while True:
            self.mostrar_menu()
            try:
                opcao = input("Escolha uma opção: ").strip()
                funcao = self.funcoes.get(opcao)
                if funcao:
                    funcao()
                else:
                    print("Opção inválida. Tente novamente.")
            except KeyboardInterrupt:
                print("\n\nInterrompido pelo usuário.")
                break
            except Exception as e:
                logger.error(f"Erro inesperado: {e}")


def main():
    """Ponto de entrada principal."""
    ferramenta = FerramentaIntegrada()
    ferramenta.executar()


if __name__ == "__main__":
    main()