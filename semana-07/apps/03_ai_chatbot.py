import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError


load_dotenv()
st.set_page_config(page_title="AI SOC Chatbot", page_icon="🤖", layout="centered")


def load_openai_client() -> OpenAI | None:
    """Carrega a chave do OpenAI via .env e cria o cliente."""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("OPENAI_API_KEY não encontrada no arquivo .env.")
            return None
        return OpenAI(api_key=api_key, timeout=30.0)
    except Exception as exc:
        st.error(f"Erro ao inicializar cliente OpenAI: {exc}")
        return None


def ask_openai(client: OpenAI, history: list) -> str:
    """Consulta o modelo OpenAI com tratamento de exceções."""
    try:
        # Adicionamos a mensagem de sistema ao histórico enviado
        messages = [{"role": "system", "content": "Você é um assistente de segurança cibernética."}]
        messages.extend(history)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=700,
        )
        return response.choices[0].message.content or "Nenhuma resposta recebida."
    except APITimeoutError:
        return "Tempo limite excedido ao consultar a IA."
    except APIConnectionError:
        return "Falha de conexão com a API da OpenAI."
    except APIError as exc:
        return f"Erro da OpenAI: {exc}"
    except Exception as exc:
        return f"Erro inesperado: {exc}"


def main() -> None:
    st.title("🤖 Chatbot de Segurança com OpenAI")
    st.caption("Converse com um assistente de TI e registre o histórico em memória da sessão.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    client = load_openai_client()
    if client is None:
        return

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Digite sua pergunta de segurança...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("Consultando a IA..."):
            answer = ask_openai(client, st.session_state.messages)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)


if __name__ == "__main__":
    main()
