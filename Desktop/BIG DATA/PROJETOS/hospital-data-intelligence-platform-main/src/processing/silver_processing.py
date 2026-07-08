from pathlib import Path
import pandas as pd


BRONZE_DIR = Path("data/bronze")
SILVER_DIR = Path("data/silver")


def get_latest_bronze_file():
    files = list(BRONZE_DIR.glob("hospital_bronze_*.csv"))
    if not files:
        raise FileNotFoundError("Nenhum arquivo Bronze encontrado.")
    return max(files, key=lambda file: file.stat().st_mtime)


def process_bronze_to_silver():
    bronze_file = get_latest_bronze_file()
    SILVER_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(bronze_file)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    df = df.drop_duplicates()

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    df["_pipeline_layer"] = "silver"

    output_path = SILVER_DIR / "hospital_silver.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Camada Silver criada com sucesso: {output_path}")
    print(f"Arquivo Bronze usado: {bronze_file}")
    print(f"Total de registros Silver: {len(df)}")

    return output_path


if __name__ == "__main__":
    process_bronze_to_silver()