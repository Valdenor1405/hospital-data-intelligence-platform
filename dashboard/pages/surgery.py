import plotly.express as px
import streamlit as st

from services.duckdb_service import query
from components.filters import build_filter_where
from utils.formatters import format_currency, format_number


def render_surgery_page(filters):
    st.header("Centro Cirúrgico")

    where_clause = build_filter_where(filters)

    kpis = query(f"""
        SELECT
            COUNT(*) AS total_cirurgias,
            SUM(fc.custo_procedimentos) AS custo_total_cirurgias,
            AVG(fc.custo_procedimentos) AS custo_medio_cirurgia
        FROM fato_cirurgia fc
        JOIN dim_hospital dh ON fc.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fc.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON fc.sk_medico = dm.sk_medico
        {where_clause}
    """)

    c1, c2, c3 = st.columns(3)
    c1.metric("Cirurgias", format_number(kpis["total_cirurgias"][0]))
    c2.metric("Custo Total", format_currency(kpis["custo_total_cirurgias"][0]))
    c3.metric("Custo Médio", format_currency(kpis["custo_medio_cirurgia"][0]))

    st.divider()

    df_procedimento = query(f"""
        SELECT
            dp.procedimento,
            dh.hospital,
            COUNT(*) AS total_cirurgias,
            SUM(fc.custo_procedimentos) AS custo_total
        FROM fato_cirurgia fc
        JOIN dim_procedimento dp ON fc.sk_procedimento = dp.sk_procedimento
        JOIN dim_hospital dh ON fc.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fc.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON fc.sk_medico = dm.sk_medico
        {where_clause}
        GROUP BY dp.procedimento, dh.hospital
        ORDER BY custo_total DESC
    """)

    fig1 = px.bar(
        df_procedimento,
        x="procedimento",
        y="custo_total",
        color="hospital",
        title="Custos Cirúrgicos por Procedimento e Hospital",
    )
    st.plotly_chart(fig1, width="stretch")

    df_hospital = query(f"""
        SELECT
            dh.hospital,
            COUNT(*) AS total_cirurgias,
            SUM(fc.custo_procedimentos) AS custo_total
        FROM fato_cirurgia fc
        JOIN dim_hospital dh ON fc.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fc.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON fc.sk_medico = dm.sk_medico
        {where_clause}
        GROUP BY dh.hospital
        ORDER BY total_cirurgias DESC
    """)

    fig2 = px.pie(
        df_hospital,
        names="hospital",
        values="total_cirurgias",
        title="Distribuição de Cirurgias por Hospital",
    )
    st.plotly_chart(fig2, width="stretch")

    st.subheader("Tabela Centro Cirúrgico")
    st.dataframe(df_procedimento, width="stretch")