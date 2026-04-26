import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/sp500brl.csv')

SP500_FILE = DATA_DIR / 'S&P 500 Historical Data day.csv'
USDBRL_FILE = DATA_DIR / 'USD_BRL Historical Data day.csv'

def ingest_sp500brl() -> pd.DataFrame:
    sp500_df = pd.read_csv(SP500_FILE, usecols=['Date', 'Price'])
    usdbrl_df = pd.read_csv(USDBRL_FILE, usecols=['Date', 'Price'])
    
    sp500_df['date'] = pd.to_datetime(sp500_df['Date'])
    usdbrl_df['date'] = pd.to_datetime(usdbrl_df['Date'])
    
    sp500_df['price'] = sp500_df['Price'].astype(str).str.replace(',', '').astype(float)
    usdbrl_df['usdbrl_price'] = usdbrl_df['Price'].astype(float)
    
    sp500_df = sp500_df[['date', 'price']]
    usdbrl_df = usdbrl_df[['date', 'usdbrl_price']]
    
    merged_df = pd.merge(sp500_df, usdbrl_df, on='date', how='inner')
    
    merged_df['price'] = merged_df['price'] * merged_df['usdbrl_price']
    
    result_df = merged_df[['date', 'price']].sort_values('date').reset_index(drop=True)
    
    OUT.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(OUT, index=False)
    return result_df
