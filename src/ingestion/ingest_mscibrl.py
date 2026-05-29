import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/mscibrl.csv')

MSCI_FILES = [
    DATA_DIR / 'MSCI All-Country World Equity Index Historical Data.csv',
]

USDBRL_FILES = [
    DATA_DIR / 'USD_BRL Historical Data day.csv',
     DATA_DIR / 'USD_BRL Historical Data day 2.csv'
]

def ingest_mscibrl() -> pd.DataFrame:
    msci_frames = []
    for f in MSCI_FILES:
        df = pd.read_csv(f, usecols=['Date', 'Price'])
        msci_frames.append(df)
    msci_df = pd.concat(msci_frames)

    usdbrl_frames = []
    for f in USDBRL_FILES:
        df = pd.read_csv(f, usecols=['Date', 'Price'])
        usdbrl_frames.append(df)
    usdbrl_df = pd.concat(usdbrl_frames)

    msci_df['date'] = pd.to_datetime(msci_df['Date'])
    usdbrl_df['date'] = pd.to_datetime(usdbrl_df['Date'])

    msci_df['price'] = msci_df['Price'].astype(str).str.replace(',', '').astype(float)
    usdbrl_df['usdbrl_price'] = usdbrl_df['Price'].astype(float)

    msci_df = msci_df[['date', 'price']].drop_duplicates(subset='date')
    usdbrl_df = usdbrl_df[['date', 'usdbrl_price']].drop_duplicates(subset='date')

    merged_df = pd.merge(msci_df, usdbrl_df, on='date', how='inner')

    merged_df['price'] = merged_df['price'] * merged_df['usdbrl_price']

    result_df = merged_df[['date', 'price']].sort_values('date').reset_index(drop=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(OUT, index=False)
    return result_df
