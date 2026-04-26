import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/sp500.csv')

SOURCE_FILE = DATA_DIR / 'S&P 500 Historical Data day.csv'

def ingest_sp500() -> pd.DataFrame:
    df = pd.read_csv(SOURCE_FILE, usecols=['Date', 'Price'])
    df['date'] = pd.to_datetime(df['Date'])
    df['price'] = df['Price'].astype(str).str.replace(',', '').astype(float)
    df = df[['date', 'price']].sort_values('date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df
