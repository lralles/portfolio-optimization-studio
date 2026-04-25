import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/usdbrl.csv')

SOURCE_FILE = DATA_DIR / 'USD_BRL Historical Data day.csv'

def ingest_usdbrl():
    df = pd.read_csv(SOURCE_FILE, usecols=['Date', 'Price'])
    df['date'] = pd.to_datetime(df['Date'])
    df['price'] = df['Price'].astype(float)
    df = df[['date', 'price']].sort_values('date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df
