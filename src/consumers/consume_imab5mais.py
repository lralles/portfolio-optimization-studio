import pandas as pd
from pathlib import Path
from . import IndexData

def consume_imab5mais() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/imab5mais.csv'), parse_dates=['date'])
    return IndexData(name='imab5mais', data=df)
