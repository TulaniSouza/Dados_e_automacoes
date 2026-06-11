import pandas as pd
import streamlit as st


st.set_page_config(page_title="Cyber Attack Dashboard", page_icon="🛡️", layout="wide")


@st.cache_data
def load_sample_data() -> pd.DataFrame:
    """Gera um dataset de exemplo para o dashboard."""
    try:
        return pd.DataFrame(
            [
                {"date": "2026-05-01", "attack_type": "Phishing", "severity": "Alta", "source_region": "América do Norte", "affected_assets": 12, "damage_usd": 12000},
                {"date": "2026-05-02", "attack_type": "Ransomware", "severity": "Crítica", "source_region": "Europa", "affected_assets": 28, "damage_usd": 54000},
                {"date": "2026-05-03", "attack_type": "DDoS", "severity": "Média", "source_region": "Ásia", "affected_assets": 8, "damage_usd": 9000},
                {"date": "2026-05-04", "attack_type": "Phishing", "severity": "Alta", "source_region": "América Latina", "affected_assets": 14, "damage_usd": 16000},
                {"date": "2026-05-05", "attack_type": "Malware", "severity": "Crítica", "source_region": "Europa", "affected_assets": 22, "damage_usd": 43000},
            ]
        )
    except Exception as exc:
        st.error(f"Erro ao carregar dados: {exc}")
        return pd.DataFrame()


def main() -> None:
    st.title("🛡️ Dashboard de Ataques Cibernéticos")
    st.caption("KPIs, filtros interativos e visão de riscos para triagem de segurança.")

    df = load_sample_data()
    if df.empty:
        return

    st.sidebar.header("Filtros")
    severity = st.sidebar.multiselect("Severidade", sorted(df["severity"].unique()), default=sorted(df["severity"].unique()))
    region = st.sidebar.multiselect("Região", sorted(df["source_region"].unique()), default=sorted(df["source_region"].unique()))
    attack_type = st.sidebar.multiselect("Tipo de ataque", sorted(df["attack_type"].unique()), default=sorted(df["attack_type"].unique()))

    filtered = df[df["severity"].isin(severity) & df["source_region"].isin(region) & df["attack_type"].isin(attack_type)].copy()

    total_incidents = int(filtered["affected_assets"].sum())
    total_damage = int(filtered["damage_usd"].sum())
    critical_events = int(filtered[filtered["severity"] == "Crítica"].shape[0])

    c1, c2, c3 = st.columns(3)
    c1.metric("Ativos afetados", total_incidents)
    c2.metric("Danos estimados", f"US$ {total_damage:,}")
    c3.metric("Eventos críticos", critical_events)

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    by_type = filtered.groupby("attack_type", as_index=False).agg(events=("attack_type", "count"), damage=("damage_usd", "sum"))
    st.bar_chart(by_type.set_index("attack_type")["damage"])


if __name__ == "__main__":
    main()
