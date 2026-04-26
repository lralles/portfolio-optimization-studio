import pandas as pd
from pathlib import Path
from . import IndexData

def consume_usdbrl() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/usdbrl.csv'), parse_dates=['date'])
    return IndexData(name='usdbrl', data=df)
