import pandas as pd
import plotly.express as px
import streamlit as st

from pathlib import Path
from utils.formatters import format_number, format_percent


SILVER_PATH = Path("data/silver/hospital_silver.csv")


def render_quality_page(filters):
    st.header("Data Quality")

    if not SILVER_PATH.exists():
        st.error("Arquivo Silver não encontrado. Execute primeiro: python run_pipeline.py")
        return

    df = pd.read_csv(SILVER_PATH)

    total_registros = len(df)
    total_colunas = len(df.columns)
    total_nulos = int(df.isnull().sum().sum())
    total_duplicados = int(df.duplicated().sum())

    score = 100

    if total_nulos > 0:
        score -= 20

    if total_duplicados > 0:
        score -= 20

    score = max(score, 0)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Registros", format_number(total_registros))
    c2.metric("Colunas", format_number(total_colunas))
    c3.metric("Nulos", format_number(total_nulos))
    c4.metric("Duplicados", format_number(total_duplicados))
    c5.metric("Quality Score", format_percent(score))

    st.divider()

    nulls = pd.DataFrame({
        "coluna": df.columns,
        "nulos": df.isnull().sum().values,
        "tipo": [str(t) for t in df.dtypes.values],
    })

    fig1 = px.bar(
        nulls,
        x="coluna",
        y="nulos",
        title="Valores Nulos por Coluna",
    )
    st.plotly_chart(fig1, width="stretch")

    st.subheader("Perfil das Colunas")
    st.dataframe(nulls, width="stretch")

    st.subheader("Amostra da Camada Silver")
    st.dataframe(df.head(50), width="stretch")