from dataclasses import dataclass
from typing import Dict, Optional
import pandas as pd


@dataclass
class RiskReturnSlidingWindowResult:
    results: Dict[str, pd.DataFrame]
    window_years: float
    start_date: pd.Timestamp
    end_date: pd.Timestamp
    window_count: Optional[int]
    independend_windows: bool


def print_results(result: RiskReturnSlidingWindowResult) -> None:
    print("=" * 60)
    print("RISK RETURN SLIDING WINDOW")
    print("=" * 60)
    print(f"Window: {result.window_years:.4g} year(s)")
    print(f"Period: {result.start_date.date()} to {result.end_date.date()}")
    print(f"window_count: {result.window_count}")
    print(f"independend_windows: {result.independend_windows}")
    for name, df in result.results.items():
        if len(df) == 0:
            continue
        first = df.iloc[0]
        last = df.iloc[-1]
        print(
            f"{name}: {len(df)} windows | start (risk={first['annualized_volatility']:.2f}%, return={first['annualized_return']:.2f}%) "
            f"-> end (risk={last['annualized_volatility']:.2f}%, return={last['annualized_return']:.2f}%)"
        )
