import pandas as pd
from pathlib import Path
from . import IndexData

def consume_irfm1() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/irfm1.csv'), parse_dates=['date'])
    return IndexData(name='irfm1', data=df)
