<div align="center">

# Hospital Data Intelligence Platform

### Enterprise Data Engineering • Analytics • AI • MLOps

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Enterprise-green.svg)]()
[![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-orange.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)]()
[![GitHub Actions](https://img.shields.io/badge/CI-CD-success.svg)]()
[![Data Warehouse](https://img.shields.io/badge/Data-Warehouse-purple.svg)]()
[![Lakehouse](https://img.shields.io/badge/Lakehouse-Bronze%20Silver%20Gold-gold.svg)]()

---

## Enterprise Healthcare Data Engineering Platform

Modern healthcare data platform that simulates a large hospital network using modern Data Engineering, Analytics, Data Warehouse, APIs, Executive Dashboards and Machine Learning concepts.

Designed to demonstrate enterprise-grade architecture for recruiters, hiring managers and technical interviews.

</div>

---

# Architecture

```text
                           Hospital Data Intelligence Platform

             Hospital Systems (Synthetic Data Generator)
                               │
                               ▼
                        RAW DATA LAYER
                               │
                               ▼
                      BRONZE INGESTION
                               │
                               ▼
                       SILVER PROCESSING
                               │
                               ▼
                      DATA QUALITY LAYER
                               │
                               ▼
                          GOLD KPIs
                               │
                               ▼
                  ENTERPRISE DATA WAREHOUSE
                               │
                               ▼
                          DuckDB Analytics
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
             FastAPI API              Executive Dashboard
```

---

# Tech Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python |
| API | FastAPI |
| Dashboard | Streamlit |
| Analytics | DuckDB |
| Data Processing | Pandas |
| Visualization | Plotly |
| Testing | Pytest |
| Containerization | Docker |
| CI/CD | GitHub Actions |

---

# Data Lakehouse

The project follows the Medallion Architecture.

```
RAW
   │
   ▼
BRONZE
   │
   ▼
SILVER
   │
   ▼
DATA QUALITY
   │
   ▼
GOLD
   │
   ▼
ENTERPRISE DATA WAREHOUSE
```

---

# Enterprise Data Warehouse

## Dimensions

- DimPaciente
- DimHospital
- DimTempo
- DimMedico
- DimConvenio
- DimCID
- DimMedicamento
- DimProcedimento
- DimLeito

## Facts

- FatoInternacao
- FatoCirurgia
- FatoExame
- FatoFinanceiro
- FatoFarmacia
- FatoReadmissao

---

# Project Structure

```
hospital-data-intelligence-platform/

├── dashboard/
├── docs/
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── warehouse/
│
├── src/
│   ├── ingestion/
│   ├── processing/
│   ├── quality/
│   ├── transformations/
│   └── api/
│
├── tests/
├── reports/
├── configs/
├── models/
└── run_pipeline.py
```

---

# Data Pipeline

The complete pipeline performs:

- Synthetic Hospital Data Generation
- Bronze Ingestion
- Silver Transformation
- Data Quality Validation
- Gold KPI Generation
- Enterprise Data Warehouse
- DuckDB Loading
- API Exposure
- Executive Dashboard

---

# Features

- Enterprise Lakehouse

- Data Quality

- Enterprise Data Warehouse

- DuckDB Analytical Database

- FastAPI REST API

- Interactive Dashboard

- Automated Tests

- Docker Support

- GitHub Actions

---

# Dashboard Modules

- Executive Overview
- Finance
- Clinical Analytics
- Pharmacy
- Surgery Center
- Readmission
- Data Quality

---

# Machine Learning

Current features

- Readmission prediction
- Hospital KPIs
- Data Analytics

Planned

- MLflow
- SHAP
- Feature Store
- Model Registry
- Drift Monitoring

---

# How to Run

Clone repository

```bash
git clone https://github.com/Valdenor1405/hospital-data-intelligence-platform.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Execute pipeline

```bash
python run_pipeline.py
```

Start API

```bash
python -m uvicorn src.api.main:app --reload
```

Swagger

```
http://localhost:8000/docs
```

Dashboard

```bash
streamlit run dashboard/app.py
```

---

# Tests

```bash
python -m pytest -v
```

---

# Project Roadmap

## Version 1.0

- Lakehouse
- Data Warehouse
- DuckDB
- Dashboard
- API
- Data Quality

---

## Version 2.0

- PostgreSQL
- SQLAlchemy
- Alembic
- Enterprise Dashboard

---

## Version 3.0

- MLflow
- SHAP
- Feature Store
- Model Registry

---

## Version 4.0

- Apache Airflow
- Kafka
- Prometheus
- Grafana

---

## Version 5.0

- Azure
- Databricks
- Terraform
- CI/CD Enterprise

---

# Repository Statistics

Current Architecture

✔ Enterprise Data Engineering

✔ Lakehouse Architecture

✔ Enterprise Data Warehouse

✔ Analytics Database

✔ FastAPI

✔ Streamlit

✔ Docker

✔ GitHub Actions

---

## Technical Notebook

O projeto inclui um notebook técnico completo para facilitar a avaliação por recrutadores e equipes técnicas.

Arquivo:

Hospital_Data_Intelligence_Platform_Guia_Recrutador.ipynb

Conteúdo:

- Visão geral da arquitetura
- Pipeline Bronze → Silver → Gold
- Data Warehouse
- DuckDB
- Dashboard Enterprise
- FastAPI
- Roadmap do projeto
- Tecnologias utilizadas

# Author

**Valdenor Filho**

Data Engineering • AI • Analytics • DevOps

GitHub

https://github.com/Valdenor1405

LinkedIn

(https://www.linkedin.com/in/valdenor-aquino/)

---

# License

MIT License

---

If you like this project, consider giving it a Star.