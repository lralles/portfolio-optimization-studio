from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class RentabilityResult:
    filtered_df: pd.DataFrame
    rentability: pd.DataFrame
    total_return: float
    annualized_return: float
    annualized_volatility: float
    start_date: Optional[str]
    end_date: Optional[str]


def print_results(result: RentabilityResult) -> None:
    print("=" * 60)
    print("RENTABILITY ANALYSIS")
    print("=" * 60)
    print(f"Period filter: {result.start_date} to {result.end_date}")
    print(f"Observations: {len(result.filtered_df)}")
    print(f"Total return: {result.total_return:.2f}%")
    print(f"Annualized return: {result.annualized_return:.2f}%")
    print(f"Annualized volatility (risk): {result.annualized_volatility:.2f}%")
