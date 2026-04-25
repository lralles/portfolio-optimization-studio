import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/ifix.csv')

SOURCE_FILE = DATA_DIR / 'BM&FBOVESPA Real Estate IFIX Historical Data day.csv'

def ingest_ifix():
    df = pd.read_csv(SOURCE_FILE, usecols=['Date', 'Price'])
    df['date'] = pd.to_datetime(df['Date'])
    df['price'] = df['Price'].astype(str).str.replace(',', '').astype(float)
    df = df[['date', 'price']].sort_values('date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df
