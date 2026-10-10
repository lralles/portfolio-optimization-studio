from pathlib import Path

import pandas as pd

from . import IndexData


def consume_idkaipca3() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/idkaipca3.csv'), parse_dates=['date'])
    df['date'] = df['date'].astype('datetime64[ns]')
    return IndexData(name='idkaipca3', data=df)
