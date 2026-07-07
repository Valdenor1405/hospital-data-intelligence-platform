from pathlib import Path
import pandas as pd


SILVER_PATH = Path("data/silver/hospital_silver.csv")


def validate_data():
    """
    Executa validações de qualidade dos dados da camada Silver.
    """

    if not SILVER_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {SILVER_PATH}")

    df = pd.read_csv(SILVER_PATH)

    print("\n==============================")
    print(" DATA QUALITY REPORT")
    print("==============================")

    print(f"Total de registros: {len(df)}")
    print(f"Total de colunas: {len(df.columns)}")

    # ------------------------
    # Valores nulos
    # ------------------------

    nulls = df.isnull().sum()

    if nulls.sum() == 0:
        print("✅ Nenhum valor nulo encontrado.")
    else:
        print("⚠ Valores nulos encontrados:")
        print(nulls[nulls > 0])

    # ------------------------
    # Duplicidades
    # ------------------------

    duplicated = df.duplicated().sum()

    if duplicated == 0:
        print("✅ Nenhum registro duplicado.")
    else:
        print(f"⚠ Registros duplicados: {duplicated}")

    # ------------------------
    # Idade
    # ------------------------

    if "idade" in df.columns:

        invalid_age = df[df["idade"] < 0]

        if invalid_age.empty:
            print("✅ Idades válidas.")
        else:
            print(f"❌ Idades inválidas: {len(invalid_age)}")

    # ------------------------
    # Dias de internação
    # ------------------------

    if "dias_internacao" in df.columns:

        invalid_days = df[df["dias_internacao"] < 0]

        if invalid_days.empty:
            print("✅ Dias de internação válidos.")
        else:
            print(f"❌ Dias inválidos: {len(invalid_days)}")

    # ------------------------
    # Custos
    # ------------------------

    if "custo_total" in df.columns:

        invalid_cost = df[df["custo_total"] <= 0]

        if invalid_cost.empty:
            print("✅ Custos válidos.")
        else:
            print(f"❌ Custos inválidos: {len(invalid_cost)}")

    # ------------------------
    # Readmissão
    # ------------------------

    if "readmissao_30_dias" in df.columns:

        invalid_readmission = df[
            ~df["readmissao_30_dias"].isin([0, 1])
        ]

        if invalid_readmission.empty:
            print("✅ Campo readmissão válido.")
        else:
            print(f"❌ Valores inválidos em readmissão: {len(invalid_readmission)}")

    print("==============================")
    print(" FIM DA VALIDAÇÃO ")
    print("==============================\n")


if __name__ == "__main__":
    validate_data()