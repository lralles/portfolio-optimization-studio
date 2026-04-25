import warnings
import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/irfm1.csv')

SOURCE_FILE = DATA_DIR / 'IRFM1-HISTORICO.xls'

def ingest_irfm1():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        df = pd.read_excel(SOURCE_FILE, usecols=['Data de Referência', 'Número Índice'])
    df['date'] = pd.to_datetime(df['Data de Referência'])
    df['price'] = df['Número Índice']
    df = df[['date', 'price']].sort_values('date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df
