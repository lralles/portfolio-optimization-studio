from typing import List, Optional
import numpy as np
import pandas as pd
from itertools import product

from .type import PortfolioOptimizationResult, OptimizedPortfolioResult
from ..efficient_region.analysis import compute_efficient_region


def generate_portfolio_grid(asset_names: List[str], step_size: int = 10) -> List[dict]:
    n_assets = len(asset_names)
    
    if n_assets == 1:
        return [{asset_names[0]: 100.0}]
    
    portfolios = []
    
    steps = list(range(0, 101, step_size))
    
    for weights in product(steps, repeat=n_assets):
        if sum(weights) == 100:
            portfolio = {asset_names[i]: float(weights[i]) for i in range(n_assets)}
            if any(w > 0 for w in weights):
                portfolios.append(portfolio)
    
    return portfolios


def optimize_portfolio(
    indexes: List[dict],
    window_size: int,
    sample_number: int,
    independent_windows: bool = False,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    n_points: int = 200,
    step_size: int = 10,
    top_n: int = 10,
) -> PortfolioOptimizationResult:
    asset_names = [idx['name'] for idx in indexes]
    
    portfolios = generate_portfolio_grid(asset_names, step_size=step_size)
    
    print(f"Evaluating {len(portfolios)} portfolios...")
    
    results = []
    for i, portfolio in enumerate(portfolios):
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{len(portfolios)} portfolios evaluated")
        
        try:
            region_result = compute_efficient_region(
                indexes=indexes,
                test_portfolio=portfolio,
                window_size=window_size,
                sample_number=sample_number,
                independent_windows=independent_windows,
                start_date=start_date,
                end_date=end_date,
                n_points=n_points,
            )
            
            results.append({
                'portfolio': portfolio,
                'loss_score': region_result.portfolio_loss_score,
            })
        except Exception as e:
            continue
    
    results_sorted = sorted(results, key=lambda x: x['loss_score'])
    
    optimized_portfolios = []
    for rank, result in enumerate(results_sorted[:top_n], 1):
        optimized_portfolios.append(OptimizedPortfolioResult(
            weights=result['portfolio'],
            portfolio_loss_score=result['loss_score'],
            rank=rank,
        ))
    
    best_portfolio = optimized_portfolios[0] if optimized_portfolios else None
    
    best_portfolio_region = None
    if best_portfolio:
        best_portfolio_region = compute_efficient_region(
            indexes=indexes,
            test_portfolio=best_portfolio.weights,
            window_size=window_size,
            sample_number=sample_number,
            independent_windows=independent_windows,
            start_date=start_date,
            end_date=end_date,
            n_points=n_points,
        )
    
    region_result_sample = compute_efficient_region(
        indexes=indexes,
        test_portfolio=portfolios[0],
        window_size=window_size,
        sample_number=sample_number,
        independent_windows=independent_windows,
        start_date=start_date,
        end_date=end_date,
        n_points=n_points,
    )
    
    return PortfolioOptimizationResult(
        optimized_portfolios=optimized_portfolios,
        best_portfolio=best_portfolio,
        best_portfolio_region=best_portfolio_region,
        search_method=f"Grid Search (step_size={step_size}%)",
        num_portfolios_evaluated=len(results),
        window_size=window_size,
        sample_number=sample_number,
        independent_windows=independent_windows,
        requested_start_date=region_result_sample.requested_start_date,
        requested_end_date=region_result_sample.requested_end_date,
    )
