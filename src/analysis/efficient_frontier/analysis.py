from typing import List, Optional
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from .type import EfficientFrontierResult, PortfolioResult


def compute_efficient_frontier(
    indexes: List[dict],
    risk_free_rate: float = 0.0,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    n_points: int = 200,
) -> EfficientFrontierResult:
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

    # Find common dates across all indexes
    date_sets = []
    for name, df in dfs.items():
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered_dates = set(df[mask]['date'])
        date_sets.append(filtered_dates)
    
    # Get intersection of all date sets
    common_dates = set.intersection(*date_sets) if date_sets else set()
    common_dates_sorted = sorted(common_dates)
    
    # Store the effective dates that were actually used
    effective_start_date = common_dates_sorted[0] if common_dates_sorted else start_date
    effective_end_date = common_dates_sorted[-1] if common_dates_sorted else end_date
    
    # Filter all indexes to only common dates and calculate returns
    returns_dict = {}
    for name, df in dfs.items():
        filtered = df[df['date'].isin(common_dates)].sort_values('date').reset_index(drop=True)
        daily_returns = filtered['price'].pct_change().dropna()
        daily_returns.index = filtered['date'].iloc[1:].values
        returns_dict[name] = daily_returns

    returns_df = pd.DataFrame(returns_dict)
    names = list(returns_df.columns)
    n = len(names)

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

    def neg_sharpe(w):
        ret = portfolio_return(w)
        vol = portfolio_volatility(w)
        return -(ret - risk_free_rate) / vol

    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    bounds = tuple((0.0, 1.0) for _ in range(n))
    w0 = np.ones(n) / n

    min_var_result = minimize(portfolio_volatility, w0, method='SLSQP', bounds=bounds, constraints=constraints)
    min_var_weights = min_var_result.x
    min_var_return = portfolio_return(min_var_weights)
    min_var_vol = portfolio_volatility(min_var_weights)

    tangency_result = minimize(neg_sharpe, w0, method='SLSQP', bounds=bounds, constraints=constraints)
    tangency_weights = tangency_result.x
    tangency_return = portfolio_return(tangency_weights)
    tangency_vol = portfolio_volatility(tangency_weights)

    max_ret_idx = np.argmax(mu)
    max_ret_weights = np.zeros(n)
    max_ret_weights[max_ret_idx] = 1.0
    max_ret_return = portfolio_return(max_ret_weights)
    max_ret_vol = portfolio_volatility(max_ret_weights)

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
    frontier_df['volatility'] = frontier_vols
    frontier_df['annualized_return'] = frontier_rets

    assets_list = []
    for i, name in enumerate(names):
        w = np.zeros(n)
        w[i] = 1.0
        vol = portfolio_volatility(w)
        assets_list.append({
            'name': name,
            'annualized_return': mu[i] * 100,
            'volatility': vol * 100,
            'variance': (vol ** 2) * 10000,
        })
    assets_df = pd.DataFrame(assets_list)

    def weights_dict(w):
        return {name: round(float(w[i]) * 100, 2) for i, name in enumerate(names)}

    return EfficientFrontierResult(
        frontier=frontier_df.assign(
            volatility=lambda d: d['volatility'] * 100,
            annualized_return=lambda d: d['annualized_return'] * 100,
        ),
        assets=assets_df,
        min_variance_portfolio=PortfolioResult(
            weights=weights_dict(min_var_weights),
            annualized_return=min_var_return * 100,
            volatility=min_var_vol * 100,
            variance=(min_var_vol ** 2) * 10000,
        ),
        max_return_portfolio=PortfolioResult(
            weights=weights_dict(max_ret_weights),
            annualized_return=max_ret_return * 100,
            volatility=max_ret_vol * 100,
            variance=(max_ret_vol ** 2) * 10000,
        ),
        tangency_portfolio=PortfolioResult(
            weights=weights_dict(tangency_weights),
            annualized_return=tangency_return * 100,
            volatility=tangency_vol * 100,
            variance=(tangency_vol ** 2) * 10000,
        ),
        risk_free_rate=risk_free_rate * 100,
        start_date=start_date,
        end_date=end_date,
        effective_start_date=effective_start_date,
        effective_end_date=effective_end_date,
        num_common_dates=len(common_dates_sorted),
    )
