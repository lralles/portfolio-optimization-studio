from dataclasses import dataclass
from typing import Dict
import pandas as pd


@dataclass
class ComparativeAnalysisResult:
    results_df: pd.DataFrame
    rentability_timeseries: Dict[str, pd.DataFrame]
    start_date: pd.Timestamp
    end_date: pd.Timestamp


def print_results(result: ComparativeAnalysisResult) -> None:
    print("=" * 60)
    print("COMPARATIVE ANALYSIS")
    print("=" * 60)
    print(f"Period: {result.start_date.date()} to {result.end_date.date()}")
    print(f"Indexes: {len(result.rentability_timeseries)}")
    print(result.results_df.sort_values('annualized_return', ascending=False).to_string(index=False))
