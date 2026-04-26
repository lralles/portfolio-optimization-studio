import pandas as pd
from pathlib import Path
from . import IndexData

def consume_bovespa() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/bovespa.csv'), parse_dates=['date'])
    return IndexData(name='bovespa', data=df)
