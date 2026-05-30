from dataclasses import dataclass
from typing import List, Optional
import pandas as pd


@dataclass
class CorrelationMatrixResult:
    combined_df: pd.DataFrame
    correlation_matrix: pd.DataFrame
    start_date: Optional[str]
    end_date: Optional[str]
    interval: str
    index_names: List[str]


def print_results(result: CorrelationMatrixResult) -> None:
    print("=" * 60)
    print("CORRELATION MATRIX")
    print("=" * 60)
    print(f"Interval: {result.interval}")
    print(f"Period: {result.start_date} to {result.end_date}")
    print(f"Indexes: {', '.join(result.index_names)}")
    print(f"Observations: {len(result.combined_df)}")
    print(result.correlation_matrix.round(3).to_string())
