import plotly.express as px
import streamlit as st

from services.duckdb_service import query
from components.filters import build_filter_where
from utils.formatters import format_currency


def render_finance_page(filters):
    st.header("Financeiro")

    where_clause = build_filter_where(filters)

    kpis = query("""
        SELECT
            SUM(custo_total) AS receita_total,
            AVG(custo_total) AS ticket_medio,
            SUM(custo_medicamentos) AS custo_medicamentos,
            SUM(custo_procedimentos) AS custo_procedimentos
        FROM fato_financeiro
    """)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Receita Total", format_currency(kpis["receita_total"][0]))
    c2.metric("Ticket Médio", format_currency(kpis["ticket_medio"][0]))
    c3.metric("Custo Medicamentos", format_currency(kpis["custo_medicamentos"][0]))
    c4.metric("Custo Procedimentos", format_currency(kpis["custo_procedimentos"][0]))

    st.divider()

    df_hospital = query(f"""
        SELECT
            dh.hospital,
            SUM(ff.custo_total) AS receita_total,
            AVG(ff.custo_total) AS ticket_medio
        FROM fato_financeiro ff
        JOIN dim_hospital dh ON ff.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON ff.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON ff.sk_medico = dm.sk_medico
        {where_clause}
        GROUP BY dh.hospital
        ORDER BY receita_total DESC
    """)

    fig1 = px.bar(
        df_hospital,
        x="hospital",
        y="receita_total",
        title="Receita Total por Hospital",
    )
    st.plotly_chart(fig1, width="stretch")

    df_convenio = query(f"""
        SELECT
            dc.convenio,
            SUM(ff.custo_total) AS receita_total
        FROM fato_financeiro ff
        JOIN dim_hospital dh ON ff.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON ff.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON ff.sk_medico = dm.sk_medico
        {where_clause}
        GROUP BY dc.convenio
        ORDER BY receita_total DESC
    """)

    fig2 = px.pie(
        df_convenio,
        names="convenio",
        values="receita_total",
        title="Distribuição de Receita por Convênio",
    )
    st.plotly_chart(fig2, width="stretch")

    df_custos = query("""
        SELECT 'Diárias' AS categoria, SUM(custo_diaria) AS valor FROM fato_financeiro
        UNION ALL
        SELECT 'Exames' AS categoria, SUM(custo_exames) AS valor FROM fato_financeiro
        UNION ALL
        SELECT 'Medicamentos' AS categoria, SUM(custo_medicamentos) AS valor FROM fato_financeiro
        UNION ALL
        SELECT 'Procedimentos' AS categoria, SUM(custo_procedimentos) AS valor FROM fato_financeiro
    """)

    fig3 = px.bar(
        df_custos,
        x="categoria",
        y="valor",
        title="Composição dos Custos Hospitalares",
    )
    st.plotly_chart(fig3, width="stretch")

    st.subheader("Tabela Financeira por Hospital")
    st.dataframe(df_hospital, width="stretch")