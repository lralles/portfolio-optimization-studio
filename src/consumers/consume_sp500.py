import pandas as pd
from pathlib import Path
from . import IndexData

def consume_sp500() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/sp500.csv'), parse_dates=['date'])
    return IndexData(name='sp500', data=df)
