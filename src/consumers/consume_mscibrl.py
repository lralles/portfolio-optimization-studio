import pandas as pd
from pathlib import Path
from . import IndexData

def consume_mscibrl() -> IndexData:
    df = pd.read_csv(Path('sanitized_data/mscibrl.csv'), parse_dates=['date'])
    return IndexData(name='mscibrl', data=df)
