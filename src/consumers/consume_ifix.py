import pandas as pd
from pathlib import Path
from . import IndexData

def consume_ifix() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/ifix.csv'), parse_dates=['date'])
    return IndexData(name='ifix', data=df)
