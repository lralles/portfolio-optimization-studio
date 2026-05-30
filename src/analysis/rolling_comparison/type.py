from dataclasses import dataclass
import pandas as pd


@dataclass
class RollingComparisonResult:
    difference: pd.DataFrame
    series_a: pd.DataFrame
    series_b: pd.DataFrame
    name_a: str
    name_b: str
    window_years: float
    start_date: pd.Timestamp
    end_date: pd.Timestamp
    total_windows: int
    wins_a: int
    wins_b: int
    win_pct_a: float
    win_pct_b: float


def print_results(result: RollingComparisonResult) -> None:
    print("=" * 60)
    print("ROLLING COMPARISON")
    print("=" * 60)
    print(f"{result.name_a} vs {result.name_b}")
    print(f"Window: {result.window_years:.4g} year(s)")
    print(f"Period: {result.start_date.date()} to {result.end_date.date()}")
    print(f"Total windows: {result.total_windows}")
    print(f"{result.name_a} wins: {result.wins_a} ({result.win_pct_a:.1f}%)")
    print(f"{result.name_b} wins: {result.wins_b} ({result.win_pct_b:.1f}%)")
    print(f"Average difference: {result.difference['difference'].mean():+.2f}%")
