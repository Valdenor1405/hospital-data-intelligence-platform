# Platform Architecture

```mermaid
flowchart TD
    A[Hospital Systems<br>HIS | ERP | LIS | PACS | Pharmacy | Finance] --> B[Raw Data Layer]
    B --> C[Bronze Layer<br>Raw + Metadata]
    C --> D[Silver Layer<br>Cleaned and Standardized Data]
    D --> E[Data Quality Layer<br>Validation Rules]
    E --> F[Gold Layer<br>Business KPIs]
    F --> G[Enterprise Data Warehouse<br>Star Schema]
    G --> H[DuckDB Analytical Database]
    H --> I[FastAPI<br>Prediction and Data Services]
    H --> J[Streamlit Executive Dashboard]
    I --> J

    K[Machine Learning Layer<br>Readmission Prediction] --> I
    L[Monitoring and Observability] --> B
    L --> C
    L --> D
    L --> E
    L --> F
    L --> G
```