from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class RiskReturnAnalysisResult:
    results_df: pd.DataFrame
    start_date: Optional[pd.Timestamp]
    end_date: Optional[pd.Timestamp]


def print_results(result: RiskReturnAnalysisResult) -> None:
    print("=" * 60)
    print("RISK RETURN ANALYSIS")
    print("=" * 60)
    if result.start_date is not None and result.end_date is not None:
        print(f"Period: {result.start_date.date()} to {result.end_date.date()}")
    print(result.results_df.sort_values('annualized_return', ascending=False).to_string(index=False))
