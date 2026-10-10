from pathlib import Path

import pandas as pd

from . import IndexData


def consume_idkaipca10() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/idkaipca10.csv'), parse_dates=['date'])
    df['date'] = df['date'].astype('datetime64[ns]')
    return IndexData(name='idkaipca10', data=df)
