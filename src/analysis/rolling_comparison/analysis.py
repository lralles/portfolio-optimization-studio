from typing import Optional
import pandas as pd
import numpy as np

from .type import RollingComparisonResult


def compute_rolling_comparison(
    index_a: dict,
    index_b: dict,
    window_years: float = 3.0,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> RollingComparisonResult:
    window_days = int(round(window_years * 365.25))

    df_a = index_a['data'].sort_values('date').reset_index(drop=True)
    df_b = index_b['data'].sort_values('date').reset_index(drop=True)

    common_start = max(df_a['date'].iloc[0], df_b['date'].iloc[0])
    common_end = min(df_a['date'].iloc[-1], df_b['date'].iloc[-1])

    if start_date is not None:
        common_start = max(common_start, pd.to_datetime(start_date))
    if end_date is not None:
        common_end = min(common_end, pd.to_datetime(end_date))

    def rolling_returns(df):
        mask = (df['date'] >= common_start) & (df['date'] <= common_end)
        filtered = df[mask].reset_index(drop=True)
        dates = []
        ann_returns = []
        for i in range(len(filtered)):
            window_end_date = filtered['date'].iloc[i]
            window_start_date = window_end_date - pd.Timedelta(days=window_days)
            window = filtered[filtered['date'] >= window_start_date].iloc[:i + 1]
            if len(window) < 2:
                continue
            actual_years = (window['date'].iloc[-1] - window['date'].iloc[0]).days / 365.25
            if actual_years < window_years * 0.8:
                continue
            total_return = (window['price'].iloc[-1] / window['price'].iloc[0]) - 1
            ann_return = ((1 + total_return) ** (1 / actual_years) - 1) * 100
            dates.append(window_end_date)
            ann_returns.append(ann_return)
        return pd.DataFrame({'date': dates, 'annualized_return': ann_returns})

    series_a = rolling_returns(df_a)
    series_b = rolling_returns(df_b)

    merged = pd.merge(series_a, series_b, on='date', suffixes=('_a', '_b'))
    merged['difference'] = merged['annualized_return_a'] - merged['annualized_return_b']

    total_windows = len(merged)
    wins_a = int((merged['difference'] > 0).sum())
    wins_b = int((merged['difference'] < 0).sum())
    win_pct_a = wins_a / total_windows * 100 if total_windows > 0 else 0.0
    win_pct_b = wins_b / total_windows * 100 if total_windows > 0 else 0.0

    return RollingComparisonResult(
        difference=merged[['date', 'difference']],
        series_a=merged[['date', 'annualized_return_a']].rename(columns={'annualized_return_a': 'annualized_return'}),
        series_b=merged[['date', 'annualized_return_b']].rename(columns={'annualized_return_b': 'annualized_return'}),
        name_a=index_a['name'],
        name_b=index_b['name'],
        window_years=window_years,
        start_date=common_start,
        end_date=common_end,
        total_windows=total_windows,
        wins_a=wins_a,
        wins_b=wins_b,
        win_pct_a=win_pct_a,
        win_pct_b=win_pct_b,
    )