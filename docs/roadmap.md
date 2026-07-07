# Hospital Data Intelligence Platform - Roadmap

## Visão do Produto

A Hospital Data Intelligence Platform é uma plataforma corporativa de Engenharia de Dados, Analytics e IA para redes hospitalares.

O objetivo é integrar dados clínicos, operacionais, financeiros e logísticos em uma arquitetura moderna baseada em Lakehouse, Data Warehouse dimensional, APIs, dashboards executivos e MLOps.

## Sprints

### Sprint 1 - Foundation
- Estrutura profissional do projeto
- FastAPI
- Testes automatizados
- Docker
- GitHub Actions

### Sprint 2 - Lakehouse Pipeline
- Raw
- Bronze
- Silver
- Gold
- Data Quality
- Pipeline unificado

### Sprint 3 - Enterprise Data Warehouse
- DimPaciente
- DimHospital
- DimTempo
- DimMedico
- DimConvenio
- DimCID
- DimMedicamento
- DimProcedimento
- DimLeito
- FatoInternacao
- FatoCirurgia
- FatoExame
- FatoFinanceiro
- FatoFarmacia
- FatoReadmissao

### Sprint 4 - Analytical Database
- DuckDB
- Carga das dimensões e fatos
- Banco analítico local
- Dashboard conectado ao banco

### Sprint 5 - Executive Dashboard
- Executive Overview
- Financeiro
- Assistencial
- Farmácia
- Centro Cirúrgico
- Readmissão
- Data Quality

### Sprint 6 - PostgreSQL Enterprise
- PostgreSQL
- SQLAlchemy
- Views
- Índices
- Integridade referencial

### Sprint 7 - MLOps
- MLflow
- Registro de experimentos
- Model Registry
- SHAP
- Monitoramento de modelo

### Sprint 8 - DataOps
- Airflow
- Orquestração
- Retry
- Logs
- Alertas

### Sprint 9 - Streaming
- Kafka
- Eventos hospitalares em tempo real
- Simulação operacional

### Sprint 10 - Cloud
- Azure
- Databricks
- Terraform
- GitHub Actions
- Deploy