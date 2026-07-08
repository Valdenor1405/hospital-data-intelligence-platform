from pathlib import Path
import duckdb
import pandas as pd


WAREHOUSE_DIR = Path("data/warehouse")
DB_PATH = WAREHOUSE_DIR / "hospital_dw.duckdb"


def load_csv_to_duckdb():
    if not WAREHOUSE_DIR.exists():
        raise FileNotFoundError("Pasta data/warehouse não encontrada.")

    csv_files = list(WAREHOUSE_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError("Nenhum CSV encontrado em data/warehouse.")

    conn = duckdb.connect(str(DB_PATH))

    for csv_file in csv_files:
        table_name = csv_file.stem

        df = pd.read_csv(csv_file)

        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.register("temp_df", df)
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_df")
        conn.unregister("temp_df")

        print(f"Tabela carregada no DuckDB: {table_name} ({len(df)} registros)")

    conn.close()

    print(f"\nBanco DuckDB criado com sucesso: {DB_PATH}")


if __name__ == "__main__":
    load_csv_to_duckdb()