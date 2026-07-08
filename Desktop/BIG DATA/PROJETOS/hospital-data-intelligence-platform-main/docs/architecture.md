# Hospital Data Intelligence Platform - Architecture

## Arquitetura Geral

```text
Sistemas Hospitalares
HIS | ERP | LIS | PACS | Farmácia | Financeiro
        |
        v
Data Ingestion Layer
        |
        v
Raw Data
        |
        v
Bronze Layer
        |
        v
Silver Layer
        |
        v
Data Quality Layer
        |
        v
Gold Layer
        |
        v
Enterprise Data Warehouse
        |
        v
DuckDB Analytical Database
        |
        v
FastAPI + Streamlit Dashboard