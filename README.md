# Engenharia de Dados e IA na Saúde Hospitalar

Projeto completo para LinkedIn e GitHub simulando um ambiente hospitalar data-driven, com geração de dados, pipeline ETL, banco SQL, modelo de Machine Learning e dashboard BI.

## Objetivo

Demonstrar como Engenharia de Dados, Inteligência Artificial e Analytics podem transformar dados hospitalares em indicadores estratégicos para melhorar gestão, reduzir custos operacionais e apoiar decisões clínicas.

> Projeto educacional. Os dados são sintéticos e não representam pacientes reais.

## Arquitetura

```text
Sistemas Hospitalares / IoT / UTI / Laboratório
        ↓
Ingestão de dados CSV
        ↓
ETL com Python + Pandas
        ↓
Banco SQLite + Camada Analytics
        ↓
Machine Learning: previsão de risco de readmissão hospitalar
        ↓
Dashboard Streamlit + Relatórios
```

## Principais entregas

- Dataset hospitalar sintético com prontuário, exames, UTI, sinais vitais, custos e estoque.
- Pipeline ETL com tratamento, padronização e criação de indicadores.
- Banco de dados SQLite simulando um Data Warehouse local.
- Modelo de Machine Learning para prever risco de readmissão em até 30 dias.
- Dashboard BI com KPIs hospitalares, ocupação, custos, risco clínico e alertas.
- Notebook explicativo passo a passo para portfólio.

## Como executar

```bash
conda create -n saude-dados-ia python=3.11 -y
conda activate saude-dados-ia
pip install -r requirements.txt
python src/01_generate_data.py
python src/02_etl_pipeline.py
python src/03_train_model.py
streamlit run dashboard/app.py
```

Ou abra o notebook:

```bash
jupyter notebook notebooks/projeto_saude_hospitalar_data_engineering_ia.ipynb
```

## Resultado esperado

O projeto gera automaticamente:

- `data/raw/hospital_raw.csv`
- `data/processed/hospital_analytics.csv`
- `data/processed/hospital_dw.sqlite`
- `models/modelo_readmissao.pkl`
- gráficos em `reports/figures/`

## Tecnologias utilizadas

Python, Pandas, NumPy, SQLite, Scikit-learn, Matplotlib, Streamlit, Plotly e Joblib.

## Sugestão de postagem LinkedIn

Criei um projeto completo de Engenharia de Dados + IA aplicado à saúde hospitalar. O objetivo foi simular como hospitais podem transformar dados de prontuários, UTI, exames, custos e monitoramento de pacientes em inteligência operacional e preditiva.

O projeto contém pipeline ETL, banco SQL, modelo de Machine Learning, dashboard BI e documentação para GitHub.

Dados bem estruturados não apenas geram relatórios. Eles ajudam a salvar vidas.

#SaudeDigital #EngenhariaDeDados #InteligenciaArtificial #MachineLearning #DataEngineering #Healthcare #Analytics #BusinessIntelligence #Python #ETL #LGPD
