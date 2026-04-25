import warnings
import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/imab5mais.csv')

SOURCE_FILE = DATA_DIR / 'IMAB5MAIS-HISTORICO.xls'

def ingest_imab5mais():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        df = pd.read_excel(SOURCE_FILE, usecols=['Data de Referência', 'Número Índice'])
    df['date'] = pd.to_datetime(df['Data de Referência'])
    df['price'] = df['Número Índice']
    df = df[['date', 'price']].sort_values('date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df
