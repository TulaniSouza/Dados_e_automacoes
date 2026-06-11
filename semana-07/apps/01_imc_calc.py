import streamlit as st


st.set_page_config(page_title="IMC Visual", page_icon="⚖️", layout="wide")


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calcula o IMC e valida entradas."""
    try:
        if weight_kg <= 0 or height_m <= 0:
            raise ValueError("Peso e altura devem ser maiores que zero.")
        return round(weight_kg / (height_m ** 2), 2)
    except Exception as exc:
        st.error(f"Erro ao calcular IMC: {exc}")
        return 0.0


def bmi_category(bmi: float) -> str:
    """Classifica o IMC."""
    if bmi < 18.5:
        return "Abaixo do peso"
    if bmi < 25:
        return "Peso ideal"
    if bmi < 30:
        return "Sobrepeso"
    return "Obesidade"


def bmi_color(bmi: float) -> str:
    """Define a cor do aviso do IMC."""
    if bmi < 18.5:
        return "#f59e0b"
    if bmi < 25:
        return "#10b981"
    if bmi < 30:
        return "#f97316"
    return "#ef4444"


def main() -> None:
    st.title("⚖️ Calculadora de IMC com métricas visuais")
    st.caption("Ferramenta rápida para avaliar o índice de massa corporal com alertas coloridos.")

    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1, value=70.0)
    with col2:
        height = st.number_input("Altura (m)", min_value=0.0, step=0.01, value=1.75)

    bmi = calculate_bmi(weight, height)

    if bmi > 0:
        category = bmi_category(bmi)
        color = bmi_color(bmi)

        st.markdown(
            f"<div style='background-color:{color};padding:16px;border-radius:12px;color:white;'>"
            f"<strong>Resultado:</strong> IMC {bmi} — {category}</div>",
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("IMC", f"{bmi}")
        c2.metric("Categoria", category)
        c3.metric("Faixa sugerida", "18.5 a 24.9")

        st.progress(min(max((bmi / 40), 0.0), 1.0))
        st.write("Atenção: o IMC é uma referência rápida e não substitui avaliação médica.")


if __name__ == "__main__":
    main()
