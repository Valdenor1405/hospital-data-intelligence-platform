from pathlib import Path
import duckdb
import pandas as pd


DB_PATH = Path("data/warehouse/hospital_dw.duckdb")


def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            "Banco DuckDB não encontrado. Execute primeiro: python run_pipeline.py"
        )

    return duckdb.connect(str(DB_PATH), read_only=True)


def query(sql: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        return conn.execute(sql).fetchdf()
    finally:
        conn.close()