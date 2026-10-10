from pathlib import Path

import pandas as pd

from . import IndexData


def consume_idkaipca20() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/idkaipca20.csv'), parse_dates=['date'])
    df['date'] = df['date'].astype('datetime64[ns]')
    return IndexData(name='idkaipca20', data=df)
