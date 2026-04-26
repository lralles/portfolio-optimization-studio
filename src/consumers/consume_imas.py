import pandas as pd
from pathlib import Path
from . import IndexData

def consume_imas() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/imas.csv'), parse_dates=['date'])
    return IndexData(name='imas', data=df)
