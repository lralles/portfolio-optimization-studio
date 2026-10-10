from pathlib import Path

import pandas as pd

from . import IndexData


def consume_idkaipca5() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/idkaipca5.csv'), parse_dates=['date'])
    df['date'] = df['date'].astype('datetime64[ns]')
    return IndexData(name='idkaipca5', data=df)
