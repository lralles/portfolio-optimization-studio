from typing import TypedDict
import pandas as pd

class IndexData(TypedDict):
    name: str
    data: pd.DataFrame
