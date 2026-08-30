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
    metrics = {}
    for name, df in dfs.items():
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered = df[mask].reset_index(drop=True)

        if len(filtered) < 2:
            results[name] = pd.DataFrame(columns=['date', 'annualized_return', 'annualized_volatility'])
            metrics[name] = {
                'avg_jump_risk': 0.0,
                'avg_jump_return': 0.0,
                'avg_jump_distance': 0.0,
            }
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

        avg_jump_risk = 0.0
        avg_jump_return = 0.0
        avg_jump_distance = 0.0
        
        if len(annualized_returns) >= 2:
            risk_jumps = []
            return_jumps = []
            distance_jumps = []
            
            for i in range(1, len(annualized_returns)):
                risk_jump = abs(annualized_volatilities[i] - annualized_volatilities[i-1])
                return_jump = abs(annualized_returns[i] - annualized_returns[i-1])
                distance_jump = np.sqrt(risk_jump**2 + return_jump**2)
                
                risk_jumps.append(risk_jump)
                return_jumps.append(return_jump)
                distance_jumps.append(distance_jump)
            
            avg_jump_risk = np.mean(risk_jumps)
            avg_jump_return = np.mean(return_jumps)
            avg_jump_distance = np.mean(distance_jumps)
        
        metrics[name] = {
            'avg_jump_risk': avg_jump_risk,
            'avg_jump_return': avg_jump_return,
            'avg_jump_distance': avg_jump_distance,
        }

    return RiskReturnSlidingWindowResult(
        results=results,
        metrics=metrics,
        window_years=window_years,
        start_date=start_date,
        end_date=end_date,
        window_count=window_count,
        independend_windows=independend_windows,
    )
