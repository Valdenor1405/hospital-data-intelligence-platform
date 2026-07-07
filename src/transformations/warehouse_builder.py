from pathlib import Path
import pandas as pd


SILVER_PATH = Path("data/silver/hospital_silver.csv")
WAREHOUSE_DIR = Path("data/warehouse")


def add_surrogate_key(df: pd.DataFrame, key_name: str) -> pd.DataFrame:
    df = df.copy().reset_index(drop=True)
    df[key_name] = range(1, len(df) + 1)
    return df


def build_dimension(df: pd.DataFrame, columns: list, key_name: str, output_name: str) -> pd.DataFrame:
    existing_cols = [col for col in columns if col in df.columns]
    dim = df[existing_cols].drop_duplicates().reset_index(drop=True)
    dim = add_surrogate_key(dim, key_name)
    dim.to_csv(WAREHOUSE_DIR / output_name, index=False, encoding="utf-8")
    return dim


def build_dim_tempo(df: pd.DataFrame) -> pd.DataFrame:
    dates = pd.to_datetime(df["data_atendimento"], errors="coerce").dropna().drop_duplicates()
    dim = pd.DataFrame({"data_atendimento": dates})
    dim = dim.sort_values("data_atendimento").reset_index(drop=True)

    dim["ano"] = dim["data_atendimento"].dt.year
    dim["mes"] = dim["data_atendimento"].dt.month
    dim["dia"] = dim["data_atendimento"].dt.day
    dim["trimestre"] = dim["data_atendimento"].dt.quarter
    dim["dia_semana"] = dim["data_atendimento"].dt.day_name()
    dim["sk_tempo"] = range(1, len(dim) + 1)

    dim.to_csv(WAREHOUSE_DIR / "dim_tempo.csv", index=False, encoding="utf-8")
    return dim


def merge_key(fact: pd.DataFrame, dim: pd.DataFrame, natural_keys: list, surrogate_key: str) -> pd.DataFrame:
    return fact.merge(dim[natural_keys + [surrogate_key]], on=natural_keys, how="left")


def build_dimensional_warehouse():
    if not SILVER_PATH.exists():
        raise FileNotFoundError("Arquivo Silver não encontrado.")

    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(SILVER_PATH)

    dim_paciente = build_dimension(
        df,
        ["id_paciente", "idade", "sexo"],
        "sk_paciente",
        "dim_paciente.csv"
    )

    dim_hospital = build_dimension(
        df,
        ["hospital"],
        "sk_hospital",
        "dim_hospital.csv"
    )

    dim_medico = build_dimension(
        df,
        ["id_medico", "especialidade_medica"],
        "sk_medico",
        "dim_medico.csv"
    )

    dim_convenio = build_dimension(
        df,
        ["convenio"],
        "sk_convenio",
        "dim_convenio.csv"
    )

    dim_cid = build_dimension(
        df,
        ["cid"],
        "sk_cid",
        "dim_cid.csv"
    )

    dim_medicamento = build_dimension(
        df,
        ["medicamento_principal"],
        "sk_medicamento",
        "dim_medicamento.csv"
    )

    dim_procedimento = build_dimension(
        df,
        ["procedimento"],
        "sk_procedimento",
        "dim_procedimento.csv"
    )

    dim_leito = build_dimension(
        df,
        ["tipo_leito", "numero_leito"],
        "sk_leito",
        "dim_leito.csv"
    )

    dim_tempo = build_dim_tempo(df)

    fact = df.copy()
    fact["data_atendimento"] = pd.to_datetime(fact["data_atendimento"], errors="coerce")

    fact = merge_key(fact, dim_paciente, ["id_paciente", "idade", "sexo"], "sk_paciente")
    fact = merge_key(fact, dim_hospital, ["hospital"], "sk_hospital")
    fact = merge_key(fact, dim_medico, ["id_medico", "especialidade_medica"], "sk_medico")
    fact = merge_key(fact, dim_convenio, ["convenio"], "sk_convenio")
    fact = merge_key(fact, dim_cid, ["cid"], "sk_cid")
    fact = merge_key(fact, dim_medicamento, ["medicamento_principal"], "sk_medicamento")
    fact = merge_key(fact, dim_procedimento, ["procedimento"], "sk_procedimento")
    fact = merge_key(fact, dim_leito, ["tipo_leito", "numero_leito"], "sk_leito")
    fact = merge_key(fact, dim_tempo, ["data_atendimento"], "sk_tempo")

    base_keys = [
        "id_atendimento",
        "sk_paciente",
        "sk_hospital",
        "sk_medico",
        "sk_convenio",
        "sk_cid",
        "sk_medicamento",
        "sk_procedimento",
        "sk_leito",
        "sk_tempo",
    ]

    fato_internacao = fact[base_keys + [
        "dias_internacao",
        "passou_uti",
        "teve_cirurgia",
    ]]
    fato_internacao.to_csv(WAREHOUSE_DIR / "fato_internacao.csv", index=False, encoding="utf-8")

    fato_cirurgia = fact[fact["teve_cirurgia"] == 1][base_keys + [
        "custo_procedimentos"
    ]]
    fato_cirurgia.to_csv(WAREHOUSE_DIR / "fato_cirurgia.csv", index=False, encoding="utf-8")

    fato_exame = fact[base_keys + [
        "qtd_exames",
        "custo_exames",
        "glicose",
        "creatinina",
        "saturacao_o2",
        "frequencia_cardiaca",
        "pressao_sistolica",
    ]]
    fato_exame.to_csv(WAREHOUSE_DIR / "fato_exame.csv", index=False, encoding="utf-8")

    fato_financeiro = fact[base_keys + [
        "custo_diaria",
        "custo_exames",
        "custo_medicamentos",
        "custo_procedimentos",
        "custo_total",
    ]]
    fato_financeiro.to_csv(WAREHOUSE_DIR / "fato_financeiro.csv", index=False, encoding="utf-8")

    fato_farmacia = fact[base_keys + [
        "status_estoque_medicamentos",
        "custo_medicamentos",
    ]]
    fato_farmacia.to_csv(WAREHOUSE_DIR / "fato_farmacia.csv", index=False, encoding="utf-8")

    fato_readmissao = fact[base_keys + [
        "readmissao_30_dias",
    ]]
    fato_readmissao.to_csv(WAREHOUSE_DIR / "fato_readmissao.csv", index=False, encoding="utf-8")

    print("Data Warehouse Enterprise criado com sucesso.")
    print(f"Arquivos gerados em: {WAREHOUSE_DIR}")
    print(f"DimPaciente: {len(dim_paciente)}")
    print(f"DimHospital: {len(dim_hospital)}")
    print(f"DimTempo: {len(dim_tempo)}")
    print(f"DimMedico: {len(dim_medico)}")
    print(f"DimConvenio: {len(dim_convenio)}")
    print(f"DimCID: {len(dim_cid)}")
    print(f"DimMedicamento: {len(dim_medicamento)}")
    print(f"DimProcedimento: {len(dim_procedimento)}")
    print(f"DimLeito: {len(dim_leito)}")
    print(f"FatoInternacao: {len(fato_internacao)}")
    print(f"FatoCirurgia: {len(fato_cirurgia)}")
    print(f"FatoExame: {len(fato_exame)}")
    print(f"FatoFinanceiro: {len(fato_financeiro)}")
    print(f"FatoFarmacia: {len(fato_farmacia)}")
    print(f"FatoReadmissao: {len(fato_readmissao)}")


if __name__ == "__main__":
    build_dimensional_warehouse()