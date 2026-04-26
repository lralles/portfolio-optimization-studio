import pandas as pd
from pathlib import Path
from . import IndexData

def consume_ipca() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/ipca.csv'), parse_dates=['date'])
    return IndexData(name='ipca', data=df)
