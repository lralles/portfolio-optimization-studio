import pandas as pd
from pathlib import Path
from . import IndexData

def consume_imab() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/imab.csv'), parse_dates=['date'])
    return IndexData(name='imab', data=df)
