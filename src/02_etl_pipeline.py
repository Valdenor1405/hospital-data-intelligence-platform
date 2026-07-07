import sqlite3
from pathlib import Path
import pandas as pd

def run_etl():
    raw = Path('data/raw/hospital_raw.csv')
    processed = Path('data/processed'); processed.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(raw, parse_dates=['data_atendimento'])
    df = df.drop_duplicates('id_atendimento')
    df['mes'] = df['data_atendimento'].dt.to_period('M').astype(str)
    df['faixa_etaria'] = pd.cut(df['idade'], bins=[-1,17,39,59,120], labels=['0-17','18-39','40-59','60+'])
    df['risco_clinico_score'] = (
        (df['idade']>=60).astype(int)*2 + df['passou_uti']*3 +
        (df['saturacao_o2']<92).astype(int)*3 + (df['frequencia_cardiaca']>110).astype(int)*2 +
        (df['glicose']>180).astype(int) + (df['creatinina']>1.4).astype(int)*2
    )
    df['nivel_risco'] = pd.cut(df['risco_clinico_score'], bins=[-1,2,5,20], labels=['Baixo','Médio','Alto'])
    df['custo_por_dia'] = (df['custo_total'] / df['dias_internacao']).round(2)
    df.to_csv(processed/'hospital_analytics.csv', index=False)
    con = sqlite3.connect(processed/'hospital_dw.sqlite')
    df.to_sql('fato_atendimentos', con, if_exists='replace', index=False)
    df.groupby('setor', as_index=False).agg(atendimentos=('id_atendimento','count'), custo_medio=('custo_total','mean'), dias_medios=('dias_internacao','mean'), taxa_readmissao=('readmissao_30_dias','mean')).to_sql('vw_kpis_setor', con, if_exists='replace', index=False)
    con.close()
    print('ETL concluído: data/processed/hospital_analytics.csv e hospital_dw.sqlite')

if __name__ == '__main__':
    run_etl()
