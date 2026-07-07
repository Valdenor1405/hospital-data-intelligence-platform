from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI(
    title="Hospital Data Intelligence API",
    description="API para predição de readmissão hospitalar.",
    version="1.0.0",
)

MODEL_PATH = Path("models/modelo_readmissao.pkl")


class PatientRiskInput(BaseModel):
    idade: int
    dias_internacao: int
    custo_total: float
    exames_realizados: int
    qtd_medicamentos: int


@app.get("/")
def health_check():
    return {
        "status": "online",
        "project": "Hospital Data Intelligence Platform",
        "message": "API funcionando corretamente.",
    }


@app.post("/predict/readmission")
def predict_readmission(data: PatientRiskInput):
    if not MODEL_PATH.exists():
        return {"error": "Modelo não encontrado. Execute o treinamento antes de usar a API."}

    model = joblib.load(MODEL_PATH)

    input_df = pd.DataFrame([data.model_dump()])
    prediction = model.predict(input_df)[0]

    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(input_df)[0][1])

    return {
        "readmission_prediction": int(prediction),
        "readmission_probability": probability,
        "risk_level": "Alto" if probability and probability >= 0.7 else "Moderado/Baixo",
    }
