from dataclasses import dataclass
import pandas as pd


@dataclass
class DiscountedAnalysisResult:
    aligned: pd.DataFrame
    measured_return: pd.Series
    reference_return: pd.Series
    discounted_return: pd.Series
    results_df: pd.DataFrame
    measured_name: str
    reference_name: str
    start_date: pd.Timestamp
    end_date: pd.Timestamp


def print_results(result: DiscountedAnalysisResult) -> None:
    print("=" * 60)
    print("DISCOUNTED ANALYSIS")
    print("=" * 60)
    print(f"Measured: {result.measured_name}")
    print(f"Reference: {result.reference_name}")
    print(f"Period: {result.start_date.date()} to {result.end_date.date()}")
    print(result.results_df.to_string(index=False))
