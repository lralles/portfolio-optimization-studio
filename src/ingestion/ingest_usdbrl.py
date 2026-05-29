import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/usdbrl.csv')

SOURCE_FILES = [
    DATA_DIR / 'USD_BRL Historical Data day.csv',
    DATA_DIR / 'USD_BRL Historical Data day 2.csv'
]

def ingest_usdbrl() -> pd.DataFrame:
    frames = []
    for f in SOURCE_FILES:
        df = pd.read_csv(f, usecols=['Date', 'Price'])
        frames.append(df)
    df = pd.concat(frames)
    df['date'] = pd.to_datetime(df['Date'])
    df['price'] = df['Price'].astype(float)
    df = df[['date', 'price']].drop_duplicates(subset='date').sort_values('date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df
