from typing import List, Optional
import pandas as pd
import numpy as np

from .type import RiskReturnSlidingWindowResult


def compute_risk_return_sliding_window(
    indexes: List[dict],
    window_years: float,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    window_count: Optional[int] = None,
    independend_windows: bool = False,
) -> RiskReturnSlidingWindowResult:
    window_days = int(round(window_years * 365.25))

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

        if len(filtered) < 2:
            results[name] = pd.DataFrame(columns=['date', 'annualized_return', 'annualized_volatility'])
            continue

        dates = []
        annualized_returns = []
        annualized_volatilities = []

        valid_windows = []
        for i in range(len(filtered)):
            window_end_date = filtered['date'].iloc[i]
            window_start_date = window_end_date - pd.Timedelta(days=window_days)
            window = filtered[(filtered['date'] >= window_start_date) & (filtered['date'] <= window_end_date)]

            if len(window) < 2:
                continue

            years = (window['date'].iloc[-1] - window['date'].iloc[0]).days / 365.25
            if years < window_years * 0.8:
                continue

            total_return = (window['price'].iloc[-1] / window['price'].iloc[0]) - 1
            annualized_return = ((1 + total_return) ** (1 / years) - 1) * 100

            returns = window['price'].pct_change().dropna()
            annualized_volatility = returns.std() * (252 ** 0.5) * 100

            valid_windows.append((window['date'].iloc[0], window_end_date, annualized_return, annualized_volatility))

        if independend_windows:
            selected_windows = []
            last_end = None
            for start, end, ann_return, ann_vol in valid_windows:
                if last_end is None or start > last_end:
                    selected_windows.append((start, end, ann_return, ann_vol))
                    last_end = end
            valid_windows = selected_windows

        if window_count is not None and window_count > 0 and len(valid_windows) > 0:
            if window_count == 1:
                idx = [len(valid_windows) - 1]
            else:
                idx = np.linspace(0, len(valid_windows) - 1, window_count, dtype=int)
                idx = np.unique(idx)
            valid_windows = [valid_windows[i] for i in idx]

        for _, end, ann_return, ann_vol in valid_windows:
            dates.append(end)
            annualized_returns.append(ann_return)
            annualized_volatilities.append(ann_vol)

        results[name] = pd.DataFrame({
            'date': dates,
            'annualized_return': annualized_returns,
            'annualized_volatility': annualized_volatilities,
        })

    return RiskReturnSlidingWindowResult(
        results=results,
        window_years=window_years,
        start_date=start_date,
        end_date=end_date,
        window_count=window_count,
        independend_windows=independend_windows,
    )
