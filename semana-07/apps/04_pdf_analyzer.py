import os
from typing import Tuple

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, APITimeoutError
from pypdf import PdfReader


load_dotenv()
st.set_page_config(page_title="PDF Analyzer", page_icon="📄", layout="wide")


def extract_text_from_pdf(uploaded_file) -> str:
    """Extrai texto de um PDF com tratamento de exceções."""
    try:
        reader = PdfReader(uploaded_file)
        text_chunks = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(text_chunks)
    except Exception as exc:
        st.error(f"Erro ao ler PDF: {exc}")
        return ""


def load_openai_client() -> OpenAI | None:
    """Carrega o cliente OpenAI via .env."""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("OPENAI_API_KEY não encontrada no .env.")
            return None
        return OpenAI(api_key=api_key, timeout=30.0)
    except Exception as exc:
        st.error(f"Erro ao inicializar cliente: {exc}")
        return None


def summarize_and_classify(client: OpenAI, text: str) -> Tuple[str, str]:
    """Resumo e classificação do documento por IA."""
    try:
        prompt = (
            "Analise o texto abaixo de um documento de segurança. "
            "Sua resposta deve começar com a classificação ('Seguro', 'Suspeito' ou 'Malicioso'), "
            "seguida por um resumo conciso do documento.\n\n"
            f"{text[:8000]}"
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=700, # Ajuste conforme necessário para o resumo
            # Adicione um stop token se a classificação for sempre a primeira palavra e você quiser separá-la
            # stop=["\n"] # Isso faria o modelo parar após a primeira linha, se a classificação estiver lá
            # Para este caso, vamos apenas extrair da primeira parte da string
        )
        output = response.choices[0].message.content or "Resposta vazia."
        lines = output.splitlines()
        
        # Extração mais robusta da categoria e resumo
        if lines and len(lines[0].split()) > 0:
            first_word = lines[0].split()[0].replace(":", "").strip() # Pega a primeira palavra e remove ':'
            if first_word in ["Seguro", "Suspeito", "Malicioso"]:
                category = first_word
                summary = " ".join(lines[0].split()[1:]) + ("\n".join(lines[1:]) if len(lines) > 1 else "")
            else: # Se a primeira palavra não for uma categoria esperada, assume o output como resumo e classifica como indefinido
                category = "Indefinido"
                summary = output
        else:
            category = "Indefinido"
            summary = "Resumo indisponível."

        return summary, category
    except APITimeoutError:
        return "Timeout na análise do PDF.", "Indefinido"
    except APIConnectionError:
        return "Falha de conexão com a API OpenAI.", "Indefinido"
    except APIError as exc:
        return f"Erro da OpenAI: {exc}", "Indefinido"
    except Exception as exc:
        return f"Erro inesperado na análise: {exc}", "Indefinido"


def main() -> None:
    st.title("📄 Analisador de PDF para Segurança")
    st.caption("Extração de texto, resumo e classificação de documentos de segurança.")

    uploaded_file = st.file_uploader("Selecione um PDF", type=["pdf"])
    if not uploaded_file:
        return

    text = extract_text_from_pdf(uploaded_file)
    if not text.strip():
        st.warning("Nenhum texto foi extraído do PDF.")
        return

    st.write("Texto extraído (preview):")
    st.code(text[:3000], language="text")

    client = load_openai_client()
    if client is None:
        return

    summary, category = summarize_and_classify(client, text)
    st.subheader("Resultado da análise")
    st.metric("Classificação", category)
    st.write(summary)


if __name__ == "__main__":
    main()
