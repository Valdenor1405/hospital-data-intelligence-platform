from pathlib import Path
from datetime import datetime
import pandas as pd


RAW_PATH = Path("data/raw/hospital_raw.csv")
BRONZE_DIR = Path("data/bronze")


def ingest_raw_to_bronze():
    """
    Ingestão da camada RAW para BRONZE.
    A camada Bronze mantém os dados brutos, apenas adicionando metadados técnicos.
    """

    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {RAW_PATH}")

    BRONZE_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_PATH)

    ingestion_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ingestion_date = datetime.now().strftime("%Y%m%d")

    df["_ingestion_timestamp"] = ingestion_timestamp
    df["_source_system"] = "hospital_synthetic_raw"
    df["_pipeline_layer"] = "bronze"

    output_path = BRONZE_DIR / f"hospital_bronze_{ingestion_date}.csv"

    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Camada Bronze criada com sucesso: {output_path}")
    print(f"Total de registros ingeridos: {len(df)}")

    return output_path


if __name__ == "__main__":
    ingest_raw_to_bronze()