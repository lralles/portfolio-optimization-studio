import pandas as pd
from pathlib import Path
from . import IndexData

def consume_imab5() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/imab5.csv'), parse_dates=['date'])
    return IndexData(name='imab5', data=df)
