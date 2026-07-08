import plotly.express as px
import streamlit as st

from services.duckdb_service import query
from components.filters import build_filter_where
from utils.formatters import format_currency, format_number


def render_pharmacy_page(filters):
    st.header("Farmácia")

    where_clause = build_filter_where(filters)

    kpis = query(f"""
        SELECT
            COUNT(*) AS total_registros,
            SUM(ff.custo_medicamentos) AS custo_medicamentos,
            COUNT(DISTINCT dm.medicamento_principal) AS total_medicamentos
        FROM fato_farmacia ff
        JOIN dim_medicamento dm ON ff.sk_medicamento = dm.sk_medicamento
        JOIN dim_hospital dh ON ff.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON ff.sk_convenio = dc.sk_convenio
        JOIN dim_medico med ON ff.sk_medico = med.sk_medico
        {where_clause.replace("dm.especialidade_medica", "med.especialidade_medica")}
    """)

    c1, c2, c3 = st.columns(3)
    c1.metric("Registros Farmácia", format_number(kpis["total_registros"][0]))
    c2.metric("Custo Medicamentos", format_currency(kpis["custo_medicamentos"][0]))
    c3.metric("Medicamentos", format_number(kpis["total_medicamentos"][0]))

    st.divider()

    df_medicamentos = query(f"""
        SELECT
            dm.medicamento_principal,
            ff.status_estoque_medicamentos,
            COUNT(*) AS ocorrencias,
            SUM(ff.custo_medicamentos) AS custo_medicamentos
        FROM fato_farmacia ff
        JOIN dim_medicamento dm ON ff.sk_medicamento = dm.sk_medicamento
        JOIN dim_hospital dh ON ff.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON ff.sk_convenio = dc.sk_convenio
        JOIN dim_medico med ON ff.sk_medico = med.sk_medico
        {where_clause.replace("dm.especialidade_medica", "med.especialidade_medica")}
        GROUP BY dm.medicamento_principal, ff.status_estoque_medicamentos
        ORDER BY custo_medicamentos DESC
    """)

    fig1 = px.bar(
        df_medicamentos,
        x="medicamento_principal",
        y="custo_medicamentos",
        color="status_estoque_medicamentos",
        title="Custo de Medicamentos por Status de Estoque",
    )
    st.plotly_chart(fig1, width="stretch")

    fig2 = px.pie(
        df_medicamentos,
        names="medicamento_principal",
        values="custo_medicamentos",
        title="Participação dos Medicamentos no Custo Total",
    )
    st.plotly_chart(fig2, width="stretch")

    st.subheader("Tabela Farmácia")
    st.dataframe(df_medicamentos, width="stretch")