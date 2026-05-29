import pandas as pd
from pathlib import Path
from . import IndexData

def consume_msci() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/msci.csv'), parse_dates=['date'])
    return IndexData(name='msci', data=df)
