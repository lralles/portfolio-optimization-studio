import pandas as pd
from pathlib import Path
from . import IndexData

def consume_sp500brl() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/sp500brl.csv'), parse_dates=['date'])
    return IndexData(name='sp500brl', data=df)
