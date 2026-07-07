import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Saúde Hospitalar Data-Driven', layout='wide')
st.title('🏥 Engenharia de Dados e IA na Saúde Hospitalar')
st.caption('Dashboard BI com dados sintéticos para portfólio de Data Engineering + Machine Learning')

df = pd.read_csv('data/processed/hospital_analytics.csv')
setores = st.sidebar.multiselect('Filtrar por setor', sorted(df['setor'].unique()), default=sorted(df['setor'].unique()))
df = df[df['setor'].isin(setores)]

c1,c2,c3,c4 = st.columns(4)
c1.metric('Atendimentos', f'{len(df):,}'.replace(',','.'))
c2.metric('Custo total', f'R$ {df.custo_total.sum():,.2f}'.replace(',', 'X').replace('.', ',').replace('X','.'))
c3.metric('Média de internação', f'{df.dias_internacao.mean():.1f} dias')
c4.metric('Taxa de readmissão', f'{df.readmissao_30_dias.mean()*100:.1f}%')

st.subheader('Indicadores por setor')
kpi = df.groupby('setor', as_index=False).agg(atendimentos=('id_atendimento','count'), custo_medio=('custo_total','mean'), taxa_readmissao=('readmissao_30_dias','mean'))
st.plotly_chart(px.bar(kpi, x='setor', y='atendimentos', title='Atendimentos por setor'), use_container_width=True)
st.plotly_chart(px.bar(kpi, x='setor', y='taxa_readmissao', title='Taxa de readmissão por setor'), use_container_width=True)

st.subheader('Risco clínico')
st.plotly_chart(px.histogram(df, x='nivel_risco', color='setor', title='Distribuição do nível de risco clínico'), use_container_width=True)
st.dataframe(df.head(50), use_container_width=True)
