import pandas as pd
from pathlib import Path
from . import IndexData

def consume_irfm1mais() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/irfm1mais.csv'), parse_dates=['date'])
    return IndexData(name='irfm1mais', data=df)
