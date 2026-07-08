from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def train():
    df = pd.read_csv('data/processed/hospital_analytics.csv')
    target = 'readmissao_30_dias'
    features = ['idade','sexo','setor','convenio','dias_internacao','passou_uti','frequencia_cardiaca','saturacao_o2','pressao_sistolica','glicose','creatinina','qtd_exames','custo_total','status_estoque_medicamentos','risco_clinico_score']
    X, y = df[features], df[target]
    num = X.select_dtypes(include='number').columns.tolist()
    cat = X.select_dtypes(exclude='number').columns.tolist()
    pre = ColumnTransformer([('num', StandardScaler(), num), ('cat', OneHotEncoder(handle_unknown='ignore'), cat)])
    model = Pipeline([('preprocessamento', pre), ('modelo', RandomForestClassifier(n_estimators=250, random_state=42, class_weight='balanced'))])
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.25, random_state=42, stratify=y)
    model.fit(Xtr, ytr)
    pred = model.predict(Xte); proba = model.predict_proba(Xte)[:,1]
    Path('models').mkdir(exist_ok=True); Path('reports/figures').mkdir(parents=True, exist_ok=True)
    joblib.dump(model, 'models/modelo_readmissao.pkl')
    report = classification_report(yte, pred)
    metrics = f'Acurácia: {accuracy_score(yte,pred):.3f}\nROC AUC: {roc_auc_score(yte,proba):.3f}\n\n{report}'
    Path('reports/model_metrics.txt').write_text(metrics, encoding='utf-8')
    disp = ConfusionMatrixDisplay(confusion_matrix(yte, pred))
    disp.plot(values_format='d')
    plt.title('Matriz de Confusão - Readmissão em 30 dias')
    plt.tight_layout(); plt.savefig('reports/figures/matriz_confusao.png', dpi=160); plt.close()
    print(metrics)

if __name__ == '__main__':
    train()
