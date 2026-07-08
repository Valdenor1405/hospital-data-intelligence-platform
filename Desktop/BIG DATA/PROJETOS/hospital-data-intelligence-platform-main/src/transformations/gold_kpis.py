from pathlib import Path
import pandas as pd


SILVER_PATH = Path("data/silver/hospital_silver.csv")
GOLD_DIR = Path("data/gold")


def build_gold_kpis():
    if not SILVER_PATH.exists():
        raise FileNotFoundError("Arquivo Silver não encontrado.")

    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(SILVER_PATH)

    kpis = {
        "total_registros": [len(df)],
        "total_colunas": [len(df.columns)],
        "total_hospitais": [df["hospital"].nunique() if "hospital" in df.columns else None],
        "idade_media": [round(df["idade"].mean(), 2) if "idade" in df.columns else None],
        "tempo_medio_internacao": [round(df["dias_internacao"].mean(), 2) if "dias_internacao" in df.columns else None],
        "custo_total": [round(df["custo_total"].sum(), 2) if "custo_total" in df.columns else None],
        "custo_medio": [round(df["custo_total"].mean(), 2) if "custo_total" in df.columns else None],
        "taxa_readmissao": [round(df["readmissao_30_dias"].mean() * 100, 2) if "readmissao_30_dias" in df.columns else None],
    }

    kpi_df = pd.DataFrame(kpis)

    output_path = GOLD_DIR / "hospital_gold_kpis.csv"
    kpi_df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Camada Gold criada com sucesso: {output_path}")
    print(kpi_df)

    return output_path


if __name__ == "__main__":
    build_gold_kpis()