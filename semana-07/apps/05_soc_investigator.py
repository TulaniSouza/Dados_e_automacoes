import os

import requests
import streamlit as st
from dotenv import load_dotenv


# Carrega o .env procurando a partir do diretório atual do script
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
st.set_page_config(page_title="SOC Investigator", page_icon="🧭", layout="wide")


def get_webhook_url() -> str:
    """Carrega o webhook do n8n a partir do .env."""
    try:
        return os.getenv("N8N_WEBHOOK_URL", "").strip()
    except Exception as exc:
        st.error(f"Erro ao carregar webhook: {exc}")
        return ""


def send_to_webhook(target: str, value: str) -> dict:
    """Envia IP/URL para o webhook do n8n via POST."""
    try:
        payload = {"target": target, "value": value}
        response = requests.post(get_webhook_url(), json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"verdict": "Erro", "reason": "Tempo limite na requisição ao webhook."}
    except requests.exceptions.RequestException as exc:
        return {"verdict": "Erro", "reason": f"Falha na requisição: {exc}"}
    except ValueError:
        return {"verdict": "Erro", "reason": "Resposta inválida do webhook (JSON não parseável)."}
    except Exception as exc:
        return {"verdict": "Erro", "reason": f"Erro inesperado: {exc}"}


def main() -> None:
    st.title("🧭 SOC Investigator")
    st.caption("Triagem rápida de IP/URL conectando a interface Streamlit ao webhook do n8n.")

    target = st.radio("Tipo de análise", ["IP", "URL"], horizontal=True)
    value = st.text_input("Digite o valor a investigar", placeholder="Ex.: 8.8.8.8 ou https://example.com")

    if st.button("Enviar para investigação"):
        webhook_url = get_webhook_url()
        if not webhook_url:
            st.warning("Configure N8N_WEBHOOK_URL no arquivo .env antes de executar o envio.")
            return

        with st.spinner("Enviando para o agente da S06..."):
            result = send_to_webhook(target, value)

        verdict = result.get("verdict", "Indefinido")
        reason = result.get("reason", "Sem detalhe adicional.")

        st.subheader("Veredito da triagem")
        color = {"Seguro": "#10b981", "Suspeito": "#f59e0b", "Malicioso": "#ef4444"}.get(verdict, "#94a3b8")
        st.markdown(
            f"<div style='background-color:{color};padding:16px;border-radius:12px;color:white;'><strong>{verdict}</strong><br>{reason}</div>",
            unsafe_allow_html=True,
        )

        st.json(result)


if __name__ == "__main__":
    main()
