import os
import logging
from dotenv import load_dotenv
from anthropic import Anthropic

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_claude_client():
    """Cria e retorna o cliente da Anthropic."""
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'YOUR_ANTHROPIC_API_KEY':
        raise ValueError("ANTHROPIC_API_KEY não configurada no .env")
    return Anthropic(api_key=api_key)

def testar_claude(query):
    """Testa a API do Claude com uma consulta simples."""
    try:
        client = get_claude_client()
        message = client.messages.create(
            model="claude-3-haiku-20240307",  # Modelo gratuito/trial
            max_tokens=1000,
            temperature=0.7,
            system="Você é um assistente útil.",
            messages=[
                {"role": "user", "content": query}
            ]
        )
        return message.content[0].text
    except Exception as e:
        logging.error(f"Erro ao testar Claude: {e}")
        return None

if __name__ == "__main__":
    query = input("Digite sua consulta para testar Claude: ")
    resposta = testar_claude(query)
    if resposta:
        print(f"Resposta do Claude: {resposta}")
    else:
        print("Falha ao obter resposta do Claude.")