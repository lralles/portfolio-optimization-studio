from dataclasses import dataclass
from typing import Dict
import pandas as pd


@dataclass
class SlidingWindowResult:
    results: Dict[str, pd.DataFrame]
    window_size: int
    start_date: pd.Timestamp
    end_date: pd.Timestamp


def print_results(result: SlidingWindowResult) -> None:
    print("=" * 60)
    print("SLIDING WINDOW ANALYSIS")
    print("=" * 60)
    print(f"Window size: {result.window_size}")
    print(f"Period: {result.start_date.date()} to {result.end_date.date()}")
    for name, df in result.results.items():
        if len(df) == 0:
            continue
        print(f"{name}: {len(df)} windows, last return={df['annualized_return'].iloc[-1]:.2f}%, last vol={df['annualized_volatility'].iloc[-1]:.2f}%")
