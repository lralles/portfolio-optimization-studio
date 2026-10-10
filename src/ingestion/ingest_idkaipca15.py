import warnings
from pathlib import Path

import pandas as pd

DATA_DIR = Path('data')
OUT = Path('sanitized_data/idkaipca15.csv')

SOURCE_FILE = DATA_DIR / 'IDKAIPCA15A-HISTORICO.xls'


def ingest_idkaipca15() -> pd.DataFrame:
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        df = pd.read_excel(SOURCE_FILE, usecols=['Data de Referência', 'Número Índice'])
    df['date'] = pd.to_datetime(df['Data de Referência']).astype('datetime64[ns]')
    df['price'] = df['Número Índice']
    df = df[['date', 'price']].sort_values('date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df
