import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
OUT = Path('sanitized_data/ipca.csv')

SOURCE_FILE = DATA_DIR / 'ipca_only_values.csv'

MONTHS_PT = {
    'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
    'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
    'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
}

def _parse_pt_date(s):
    month_name, year = s.strip().split()
    return pd.Timestamp(year=int(year), month=MONTHS_PT[month_name], day=1) + pd.offsets.MonthEnd(0)

def ingest_ipca():
    df = pd.read_csv(SOURCE_FILE, header=None, names=[0, 1, 2])
    df = df[df[0] == 'Brasil'].copy()
    df['date'] = df[1].apply(_parse_pt_date)
    df['price'] = df[2].astype(float)
    df = df[['date', 'price']].sort_values('date').reset_index(drop=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    return df
