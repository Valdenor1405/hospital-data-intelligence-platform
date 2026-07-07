import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path


DB_PATH = Path("data/warehouse/hospital_dw.duckdb")

st.set_page_config(
    page_title="Hospital Data Intelligence Platform",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 Hospital Data Intelligence Platform")
st.caption("Executive Analytics • Data Warehouse • Lakehouse • AI-ready Platform")

if not DB_PATH.exists():
    st.error("Banco DuckDB não encontrado. Execute primeiro: python run_pipeline.py")
    st.stop()

conn = duckdb.connect(str(DB_PATH), read_only=True)


def query(sql: str) -> pd.DataFrame:
    return conn.execute(sql).fetchdf()


page = st.sidebar.radio(
    "Navegação",
    [
        "Executive Overview",
        "Financeiro",
        "Assistencial",
        "Farmácia",
        "Centro Cirúrgico",
        "Readmissão",
        "Data Quality",
    ],
)


if page == "Executive Overview":
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
    c1.metric("Internações", f"{int(kpis['total_internacoes'][0]):,}".replace(",", "."))
    c2.metric("Receita Total", f"R$ {kpis['receita_total'][0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    c3.metric("Ticket Médio", f"R$ {kpis['ticket_medio'][0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
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

    fig = px.bar(df_hospital, x="hospital", y="receita", title="Receita por Hospital")
    st.plotly_chart(fig, use_container_width=True)


elif page == "Financeiro":
    st.header("Financeiro")

    df = query("""
        SELECT
            dh.hospital,
            dc.convenio,
            SUM(ff.custo_total) AS custo_total,
            SUM(ff.custo_diaria) AS custo_diaria,
            SUM(ff.custo_exames) AS custo_exames,
            SUM(ff.custo_medicamentos) AS custo_medicamentos,
            SUM(ff.custo_procedimentos) AS custo_procedimentos
        FROM fato_financeiro ff
        JOIN dim_hospital dh ON ff.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON ff.sk_convenio = dc.sk_convenio
        GROUP BY dh.hospital, dc.convenio
    """)

    st.dataframe(df, use_container_width=True)

    fig = px.bar(df, x="hospital", y="custo_total", color="convenio", title="Custo Total por Hospital e Convênio")
    st.plotly_chart(fig, use_container_width=True)


elif page == "Assistencial":
    st.header("Assistencial")

    df = query("""
        SELECT
            dm.especialidade_medica,
            dcid.cid,
            COUNT(*) AS atendimentos,
            AVG(fi.dias_internacao) AS tempo_medio
        FROM fato_internacao fi
        JOIN dim_medico dm ON fi.sk_medico = dm.sk_medico
        JOIN dim_cid dcid ON fi.sk_cid = dcid.sk_cid
        GROUP BY dm.especialidade_medica, dcid.cid
        ORDER BY atendimentos DESC
    """)

    st.dataframe(df, use_container_width=True)

    fig = px.bar(df.head(20), x="especialidade_medica", y="atendimentos", color="cid", title="Atendimentos por Especialidade e CID")
    st.plotly_chart(fig, use_container_width=True)


elif page == "Farmácia":
    st.header("Farmácia")

    df = query("""
        SELECT
            dm.medicamento_principal,
            ff.status_estoque_medicamentos,
            COUNT(*) AS ocorrencias,
            SUM(ff.custo_medicamentos) AS custo_medicamentos
        FROM fato_farmacia ff
        JOIN dim_medicamento dm ON ff.sk_medicamento = dm.sk_medicamento
        GROUP BY dm.medicamento_principal, ff.status_estoque_medicamentos
        ORDER BY custo_medicamentos DESC
    """)

    st.dataframe(df, use_container_width=True)

    fig = px.bar(df, x="medicamento_principal", y="custo_medicamentos", color="status_estoque_medicamentos", title="Custo de Medicamentos por Estoque")
    st.plotly_chart(fig, use_container_width=True)


elif page == "Centro Cirúrgico":
    st.header("Centro Cirúrgico")

    df = query("""
        SELECT
            dp.procedimento,
            dh.hospital,
            COUNT(*) AS total_cirurgias,
            SUM(fc.custo_procedimentos) AS custo_cirurgias
        FROM fato_cirurgia fc
        JOIN dim_procedimento dp ON fc.sk_procedimento = dp.sk_procedimento
        JOIN dim_hospital dh ON fc.sk_hospital = dh.sk_hospital
        GROUP BY dp.procedimento, dh.hospital
        ORDER BY custo_cirurgias DESC
    """)

    st.dataframe(df, use_container_width=True)

    fig = px.bar(df, x="procedimento", y="custo_cirurgias", color="hospital", title="Custos Cirúrgicos por Procedimento")
    st.plotly_chart(fig, use_container_width=True)


elif page == "Readmissão":
    st.header("Readmissão")

    df = query("""
        SELECT
            dh.hospital,
            dc.convenio,
            AVG(fr.readmissao_30_dias) * 100 AS taxa_readmissao
        FROM fato_readmissao fr
        JOIN dim_hospital dh ON fr.sk_hospital = dh.sk_hospital
        JOIN dim_convenio dc ON fr.sk_convenio = dc.sk_convenio
        GROUP BY dh.hospital, dc.convenio
        ORDER BY taxa_readmissao DESC
    """)

    st.dataframe(df, use_container_width=True)

    fig = px.bar(df, x="hospital", y="taxa_readmissao", color="convenio", title="Taxa de Readmissão por Hospital e Convênio")
    st.plotly_chart(fig, use_container_width=True)


elif page == "Data Quality":
    st.header("Data Quality")

    silver = pd.read_csv("data/silver/hospital_silver.csv")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registros", len(silver))
    c2.metric("Colunas", len(silver.columns))
    c3.metric("Nulos", int(silver.isnull().sum().sum()))
    c4.metric("Duplicados", int(silver.duplicated().sum()))

    st.dataframe(
        pd.DataFrame({
            "coluna": silver.columns,
            "nulos": silver.isnull().sum().values,
            "tipo": [str(t) for t in silver.dtypes.values],
        }),
        use_container_width=True,
    )