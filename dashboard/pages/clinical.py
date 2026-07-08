import plotly.express as px
import streamlit as st

from services.duckdb_service import query
from components.filters import build_filter_where
from utils.formatters import format_number


def render_clinical_page(filters):
    st.header("Assistencial")

    where_clause = build_filter_where(filters)

    kpis = query(f"""
        SELECT
            COUNT(*) AS total_internacoes,
            AVG(fi.dias_internacao) AS tempo_medio,
            SUM(fi.passou_uti) AS total_uti,
            SUM(fi.teve_cirurgia) AS total_cirurgias
        FROM fato_internacao fi
        JOIN dim_hospital dh ON fi.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fi.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON fi.sk_medico = dm.sk_medico
        {where_clause}
    """)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Internações", format_number(kpis["total_internacoes"][0]))
    c2.metric("Tempo Médio", f"{kpis['tempo_medio'][0]:.1f} dias")
    c3.metric("Passagens por UTI", format_number(kpis["total_uti"][0]))
    c4.metric("Cirurgias", format_number(kpis["total_cirurgias"][0]))

    st.divider()

    df_especialidade = query(f"""
        SELECT
            dm.especialidade_medica,
            COUNT(*) AS atendimentos,
            AVG(fi.dias_internacao) AS tempo_medio
        FROM fato_internacao fi
        JOIN dim_hospital dh ON fi.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fi.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON fi.sk_medico = dm.sk_medico
        {where_clause}
        GROUP BY dm.especialidade_medica
        ORDER BY atendimentos DESC
    """)

    fig1 = px.bar(
        df_especialidade,
        x="especialidade_medica",
        y="atendimentos",
        title="Atendimentos por Especialidade",
    )
    st.plotly_chart(fig1, width="stretch")

    df_cid = query(f"""
        SELECT
            dcid.cid,
            COUNT(*) AS atendimentos
        FROM fato_internacao fi
        JOIN dim_hospital dh ON fi.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fi.sk_convenio = dc.sk_convenio
        JOIN dim_medico dm ON fi.sk_medico = dm.sk_medico
        JOIN dim_cid dcid ON fi.sk_cid = dcid.sk_cid
        {where_clause}
        GROUP BY dcid.cid
        ORDER BY atendimentos DESC
    """)

    fig2 = px.bar(
        df_cid,
        x="cid",
        y="atendimentos",
        title="Atendimentos por CID",
    )
    st.plotly_chart(fig2, width="stretch")

    st.subheader("Indicadores Assistenciais")
    st.dataframe(df_especialidade, width="stretch")