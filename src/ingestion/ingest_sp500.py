import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/sp500.csv')

SOURCE_FILES = [
    DATA_DIR / 'S&P 500 Historical Data day.csv',
    DATA_DIR / 'S&P 500 Historical Data day 2.csv'
]

def ingest_sp500() -> pd.DataFrame:
    frames = []
    for f in SOURCE_FILES:
        df = pd.read_csv(f, usecols=['Date', 'Price'])
        frames.append(df)
    df = pd.concat(frames)
    df['date'] = pd.to_datetime(df['Date'])
    df['price'] = df['Price'].astype(str).str.replace(',', '').astype(float)
    df = df[['date', 'price']].drop_duplicates(subset='date').sort_values('date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df
