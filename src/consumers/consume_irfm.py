import pandas as pd
from pathlib import Path
from . import IndexData

def consume_irfm() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/irfm.csv'), parse_dates=['date'])
    return IndexData(name='irfm', data=df)
