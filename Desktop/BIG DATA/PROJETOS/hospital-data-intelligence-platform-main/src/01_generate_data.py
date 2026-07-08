import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

N = 5000

hospitais = [
    "Hospital São Lucas",
    "Hospital Vida Plena",
    "Hospital Santa Clara",
    "Hospital Esperança",
    "Hospital Regional Norte",
]

especialidades = [
    "Cardiologia",
    "Neurologia",
    "Ortopedia",
    "Clínica Médica",
    "Pediatria",
    "Oncologia",
    "Cirurgia Geral",
    "UTI",
]

cids = ["I10", "E11", "J18", "N18", "C50", "S72", "K35", "U07", "I21", "A09"]

procedimentos = [
    "Consulta Emergencial",
    "Internação Clínica",
    "Cirurgia Eletiva",
    "Cirurgia de Urgência",
    "Exame Laboratorial",
    "Tomografia",
    "Ressonância",
    "Hemodiálise",
]

medicamentos = [
    "Dipirona",
    "Ceftriaxona",
    "Insulina",
    "Losartana",
    "Omeprazol",
    "Morfina",
    "Heparina",
    "Furosemida",
]

tipos_leito = ["Enfermaria", "Apartamento", "UTI Adulto", "UTI Pediátrica", "Observação"]

convenios = ["SUS", "Unimed", "Bradesco Saúde", "SulAmérica", "Amil", "Particular"]

setores = ["Emergência", "UTI", "Centro Cirúrgico", "Clínica Médica", "Pediatria", "Oncologia"]

status_estoque = ["Normal", "Baixo", "Crítico"]

start_date = datetime(2025, 1, 1)

dados = []

for i in range(1, N + 1):
    idade = np.random.randint(0, 95)
    dias_internacao = np.random.randint(1, 20)
    passou_uti = np.random.choice([0, 1], p=[0.75, 0.25])
    teve_cirurgia = np.random.choice([0, 1], p=[0.70, 0.30])

    custo_diaria = dias_internacao * np.random.uniform(700, 2500)
    custo_exames = np.random.uniform(200, 4000)
    custo_medicamentos = np.random.uniform(150, 3500)
    custo_procedimentos = np.random.uniform(500, 12000) if teve_cirurgia else np.random.uniform(100, 2500)

    custo_total = custo_diaria + custo_exames + custo_medicamentos + custo_procedimentos

    data_atendimento = start_date + timedelta(days=np.random.randint(0, 365))

    dados.append({
        "id_atendimento": i,
        "id_paciente": np.random.randint(10000, 99999),
        "id_medico": np.random.randint(1000, 9999),
        "hospital": np.random.choice(hospitais),
        "data_atendimento": data_atendimento.strftime("%Y-%m-%d"),
        "idade": idade,
        "sexo": np.random.choice(["Masculino", "Feminino"]),
        "setor": np.random.choice(setores),
        "convenio": np.random.choice(convenios),
        "especialidade_medica": np.random.choice(especialidades),
        "cid": np.random.choice(cids),
        "procedimento": np.random.choice(procedimentos),
        "medicamento_principal": np.random.choice(medicamentos),
        "tipo_leito": np.random.choice(tipos_leito),
        "numero_leito": np.random.randint(1, 500),
        "dias_internacao": dias_internacao,
        "passou_uti": passou_uti,
        "teve_cirurgia": teve_cirurgia,
        "frequencia_cardiaca": np.random.randint(55, 140),
        "saturacao_o2": np.random.randint(85, 100),
        "pressao_sistolica": np.random.randint(90, 190),
        "glicose": np.random.randint(65, 280),
        "creatinina": round(np.random.uniform(0.5, 4.5), 2),
        "qtd_exames": np.random.randint(1, 25),
        "custo_diaria": round(custo_diaria, 2),
        "custo_exames": round(custo_exames, 2),
        "custo_medicamentos": round(custo_medicamentos, 2),
        "custo_procedimentos": round(custo_procedimentos, 2),
        "custo_total": round(custo_total, 2),
        "status_estoque_medicamentos": np.random.choice(status_estoque),
        "readmissao_30_dias": np.random.choice([0, 1], p=[0.72, 0.28]),
    })

df = pd.DataFrame(dados)

output_path = RAW_DIR / "hospital_raw.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Base hospitalar enterprise criada com sucesso: {output_path}")
print(f"Total de registros: {len(df)}")
print(f"Total de colunas: {len(df.columns)}")