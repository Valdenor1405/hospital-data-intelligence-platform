import plotly.express as px
import streamlit as st

from services.duckdb_service import query
from components.filters import build_filter_where
from utils.formatters import format_number, format_percent


def render_readmission_page(filters):
    st.header("Readmissão")

    where_clause = build_filter_where(filters)

    kpis = query(f"""
        SELECT
            COUNT(*) AS total_atendimentos,
            SUM(fr.readmissao_30_dias) AS total_readmissoes,
            AVG(fr.readmissao_30_dias) * 100 AS taxa_readmissao
        FROM fato_readmissao fr
        JOIN dim_hospital dh ON fr.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fr.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON fr.sk_medico = dm.sk_medico
        {where_clause}
    """)

    c1, c2, c3 = st.columns(3)
    c1.metric("Atendimentos", format_number(kpis["total_atendimentos"][0]))
    c2.metric("Readmissões", format_number(kpis["total_readmissoes"][0]))
    c3.metric("Taxa de Readmissão", format_percent(kpis["taxa_readmissao"][0]))

    st.divider()

    df_hospital = query(f"""
        SELECT
            dh.hospital,
            COUNT(*) AS atendimentos,
            SUM(fr.readmissao_30_dias) AS readmissoes,
            AVG(fr.readmissao_30_dias) * 100 AS taxa_readmissao
        FROM fato_readmissao fr
        JOIN dim_hospital dh ON fr.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fr.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON fr.sk_medico = dm.sk_medico
        {where_clause}
        GROUP BY dh.hospital
        ORDER BY taxa_readmissao DESC
    """)

    fig1 = px.bar(
        df_hospital,
        x="hospital",
        y="taxa_readmissao",
        title="Taxa de Readmissão por Hospital",
    )
    st.plotly_chart(fig1, width="stretch")

    df_convenio = query(f"""
        SELECT
            dc.convenio,
            AVG(fr.readmissao_30_dias) * 100 AS taxa_readmissao
        FROM fato_readmissao fr
        JOIN dim_hospital dh ON fr.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fr.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON fr.sk_medico = dm.sk_medico
        {where_clause}
        GROUP BY dc.convenio
        ORDER BY taxa_readmissao DESC
    """)

    fig2 = px.bar(
        df_convenio,
        x="convenio",
        y="taxa_readmissao",
        title="Taxa de Readmissão por Convênio",
    )
    st.plotly_chart(fig2, width="stretch")

    st.subheader("Tabela de Readmissão por Hospital")
    st.dataframe(df_hospital, width="stretch")