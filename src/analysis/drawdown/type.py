from dataclasses import dataclass
from typing import Optional
import pandas as pd


@dataclass
class DrawdownResult:
    filtered_df: pd.DataFrame
    drawdown: pd.DataFrame
    start_date: Optional[str]
    end_date: Optional[str]


def print_results(result: DrawdownResult) -> None:
    print("=" * 60)
    print("DRAWDOWN ANALYSIS")
    print("=" * 60)
    print(f"Period filter: {result.start_date} to {result.end_date}")
    print(f"Observations: {len(result.filtered_df)}")
    min_idx = result.drawdown['drawdown'].idxmin()
    min_date = result.drawdown.loc[min_idx, 'date']
    min_drawdown = result.drawdown.loc[min_idx, 'drawdown']
    print(f"Max drawdown: {min_drawdown:.2f}% on {min_date.date()}")
