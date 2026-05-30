from typing import List, Optional
import pandas as pd
import numpy as np

from .type import SlidingWindowResult


def compute_sliding_window(
    indexes: List[dict],
    window_size: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> SlidingWindowResult:
    dfs = {}
    for index_data in indexes:
        df = index_data['data'].sort_values('date').reset_index(drop=True)
        dfs[index_data['name']] = df

    if start_date is None:
        start_date = max(df['date'].iloc[0] for df in dfs.values())
    else:
        start_date = pd.to_datetime(start_date)

    if end_date is None:
        end_date = min(df['date'].iloc[-1] for df in dfs.values())
    else:
        end_date = pd.to_datetime(end_date)

    results = {}
    for name, df in dfs.items():
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered = df[mask].reset_index(drop=True)

        if len(filtered) < window_size + 1:
            continue

        dates = []
        annualized_returns = []
        annualized_volatilities = []

        for i in range(window_size, len(filtered)):
            window = filtered.iloc[i - window_size: i + 1]
            window_returns = window['price'].pct_change().dropna()

            total_return = (window['price'].iloc[-1] / window['price'].iloc[0]) - 1
            years = (window['date'].iloc[-1] - window['date'].iloc[0]).days / 365.25
            ann_return = ((1 + total_return) ** (1 / years) - 1) * 100 if years > 0 else 0.0
            ann_vol = window_returns.std() * (252 ** 0.5) * 100

            dates.append(window['date'].iloc[-1])
            annualized_returns.append(ann_return)
            annualized_volatilities.append(ann_vol)

        results[name] = pd.DataFrame({
            'date': dates,
            'annualized_return': annualized_returns,
            'annualized_volatility': annualized_volatilities,
        })

    return SlidingWindowResult(
        results=results,
        window_size=window_size,
        start_date=start_date,
        end_date=end_date,
    )
