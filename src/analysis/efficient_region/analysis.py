from typing import List, Optional, Dict
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from .type import EfficientRegionResult, WindowFrontierResult, PortfolioResult, IndexStats


def compute_efficient_region(
    indexes: List[dict],
    test_portfolio: Dict[str, float],
    window_size: int,
    sample_number: int,
    independent_windows: bool = False,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    n_points: int = 200,
) -> EfficientRegionResult:
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

    date_sets = []
    for name, df in dfs.items():
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_dates = set(df[mask]['date'])
        date_sets.append(filtered_dates)
    
    common_dates = set.intersection(*date_sets) if date_sets else set()
    common_dates_sorted = sorted(common_dates)
    
    if len(common_dates_sorted) < window_size:
        raise ValueError(f"Not enough common dates ({len(common_dates_sorted)}) for window size {window_size}")

    if independent_windows:
        num_windows = len(common_dates_sorted) // window_size
        window_starts = [i * window_size for i in range(num_windows)]
    else:
        if sample_number > len(common_dates_sorted) - window_size + 1:
            raise ValueError(f"sample_number ({sample_number}) too large for available dates")
        max_start = len(common_dates_sorted) - window_size
        window_starts = np.linspace(0, max_start, sample_number, dtype=int)
        num_windows = sample_number

    names = list(dfs.keys())
    n = len(names)

    test_weights_array = np.array([test_portfolio.get(name, 0.0) / 100.0 for name in names])
    if not np.isclose(test_weights_array.sum(), 1.0):
        raise ValueError(f"Test portfolio weights must sum to 100%, got {test_weights_array.sum() * 100:.2f}%")

    window_frontiers = []
    
    for window_idx, start_idx in enumerate(window_starts):
        end_idx = start_idx + window_size
        window_dates = common_dates_sorted[start_idx:end_idx]
        
        window_start_date = window_dates[0]
        window_end_date = window_dates[-1]
        
        returns_dict = {}
        for name, df in dfs.items():
            filtered = df[df['date'].isin(window_dates)].sort_values('date').reset_index(drop=True)
            daily_returns = filtered['price'].pct_change().dropna()
            daily_returns.index = filtered['date'].iloc[1:].values
            returns_dict[name] = daily_returns

        returns_df = pd.DataFrame(returns_dict)
        
        mean_daily = returns_df.mean()
        cov_daily = returns_df.cov()

        ann_mean = mean_daily * 252
        ann_cov = cov_daily * 252

        mu = ann_mean.values
        sigma = ann_cov.values

        def portfolio_volatility(w):
            return np.sqrt(w @ sigma @ w)

        def portfolio_return(w):
            return w @ mu

        constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
        bounds = tuple((0.0, 1.0) for _ in range(n))
        w0 = np.ones(n) / n

        min_var_result = minimize(portfolio_volatility, w0, method='SLSQP', bounds=bounds, constraints=constraints)
        min_var_weights = min_var_result.x
        min_var_return = portfolio_return(min_var_weights)

        max_ret_idx = np.argmax(mu)
        max_ret_weights = np.zeros(n)
        max_ret_weights[max_ret_idx] = 1.0
        max_ret_return = portfolio_return(max_ret_weights)

        target_returns = np.linspace(min_var_return, max_ret_return, n_points)
        frontier_vols = []
        frontier_rets = []
        frontier_weights = []

        for target in target_returns:
            cons = [
                {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                {'type': 'eq', 'fun': lambda w, t=target: portfolio_return(w) - t},
            ]
            res = minimize(portfolio_volatility, w0, method='SLSQP', bounds=bounds, constraints=cons)
            if res.success:
                frontier_vols.append(portfolio_volatility(res.x))
                frontier_rets.append(target)
                frontier_weights.append(res.x)

        frontier_df = pd.DataFrame(frontier_weights, columns=names)
        frontier_df['volatility'] = [v * 100 for v in frontier_vols]
        frontier_df['annualized_return'] = [r * 100 for r in frontier_rets]

        test_return = portfolio_return(test_weights_array)
        test_vol = portfolio_volatility(test_weights_array)
        
        test_portfolio_point = PortfolioResult(
            weights={name: round(float(test_weights_array[i]) * 100, 2) for i, name in enumerate(names)},
            annualized_return=test_return * 100,
            volatility=test_vol * 100,
            variance=(test_vol ** 2) * 10000,
        )

        distances = np.sqrt(
            (frontier_df['volatility'] - test_vol * 100) ** 2 + 
            (frontier_df['annualized_return'] - test_return * 100) ** 2
        )
        min_distance = distances.min()
        closest_idx = distances.idxmin()
        closest_point = (
            frontier_df.loc[closest_idx, 'volatility'],
            frontier_df.loc[closest_idx, 'annualized_return']
        )

        closest_magnitude = np.sqrt(closest_point[0] ** 2 + closest_point[1] ** 2)
        portfolio_error_score = min_distance / closest_magnitude if closest_magnitude > 0 else 0.0

        index_stats = {}
        for i, name in enumerate(names):
            single_weight = np.zeros(n)
            single_weight[i] = 1.0
            index_stats[name] = IndexStats(
                annualized_return=portfolio_return(single_weight) * 100,
                volatility=portfolio_volatility(single_weight) * 100,
            )

        window_frontiers.append(WindowFrontierResult(
            window_index=window_idx,
            start_date=window_start_date,
            end_date=window_end_date,
            frontier=frontier_df,
            test_portfolio_point=test_portfolio_point,
            distance_to_frontier=min_distance,
            closest_frontier_point=closest_point,
            portfolio_error_score=portfolio_error_score,
            index_stats=index_stats,
        ))

    assets_list = []
    for name in names:
        assets_list.append({
            'name': name,
        })
    assets_df = pd.DataFrame(assets_list)

    portfolio_loss_score = np.mean([wf.portfolio_error_score for wf in window_frontiers])

    return EfficientRegionResult(
        window_frontiers=window_frontiers,
        assets=assets_df,
        test_portfolio_weights=test_portfolio,
        window_size=window_size,
        sample_number=sample_number if not independent_windows else num_windows,
        independent_windows=independent_windows,
        requested_start_date=start_date,
        requested_end_date=end_date,
        num_windows=num_windows,
        portfolio_loss_score=portfolio_loss_score,
    )
