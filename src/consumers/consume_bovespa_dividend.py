import pandas as pd
from pathlib import Path
from . import IndexData

def consume_bovespa_dividend() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/bovespa_dividend.csv'), parse_dates=['date'])
    return IndexData(name='bovespa_dividend', data=df)
