import plotly.express as px
import streamlit as st

from services.duckdb_service import query
from utils.formatters import format_currency, format_number


def render_executive_page(filters):
    st.header("Executive Overview")

    kpis = query("""
        SELECT
            COUNT(*) AS total_internacoes,
            SUM(custo_total) AS receita_total,
            AVG(custo_total) AS ticket_medio,
            AVG(dias_internacao) AS tempo_medio_internacao,
            SUM(readmissao_30_dias) AS total_readmissoes
        FROM fato_financeiro ff
        JOIN fato_internacao fi USING(id_atendimento)
        JOIN fato_readmissao fr USING(id_atendimento)
    """)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Internações", format_number(kpis["total_internacoes"][0]))
    c2.metric("Receita Total", format_currency(kpis["receita_total"][0]))
    c3.metric("Ticket Médio", format_currency(kpis["ticket_medio"][0]))
    c4.metric("Tempo Médio", f"{kpis['tempo_medio_internacao'][0]:.1f} dias")
    c5.metric("Readmissões", int(kpis["total_readmissoes"][0]))

    st.divider()

    df_hospital = query("""
        SELECT
            dh.hospital,
            COUNT(*) AS internacoes,
            SUM(ff.custo_total) AS receita
        FROM fato_financeiro ff
        JOIN dim_hospital dh ON ff.sk_hospital = dh.sk_hospital
        GROUP BY dh.hospital
        ORDER BY receita DESC
    """)

    fig = px.bar(
        df_hospital,
        x="hospital",
        y="receita",
        title="Receita por Hospital",
    )

    st.plotly_chart(fig, width="stretch")