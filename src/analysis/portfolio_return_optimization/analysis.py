from typing import List, Optional
import numpy as np

from .type import PortfolioReturnOptimizationResult, OptimizedPortfolioResult
from ..efficient_return_region.analysis import compute_efficient_return_region
from ..portfolio_optimization.analysis import generate_portfolio_grid


def optimize_portfolio_by_return(
    indexes: List[dict],
    window_size: int,
    sample_number: int,
    independent_windows: bool = False,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    n_points: int = 200,
    step_size: int = 10,
    top_n: int = 10,
) -> PortfolioReturnOptimizationResult:
    asset_names = [idx['name'] for idx in indexes]

    portfolios = generate_portfolio_grid(asset_names, step_size=step_size)

    print(f"Evaluating {len(portfolios)} portfolios...")

    results = []
    for i, portfolio in enumerate(portfolios):
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{len(portfolios)} portfolios evaluated")

        try:
            region_result = compute_efficient_return_region(
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
        except Exception:
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
        best_portfolio_region = compute_efficient_return_region(
            indexes=indexes,
            test_portfolio=best_portfolio.weights,
            window_size=window_size,
            sample_number=sample_number,
            independent_windows=independent_windows,
            start_date=start_date,
            end_date=end_date,
            n_points=n_points,
        )

    region_result_sample = compute_efficient_return_region(
        indexes=indexes,
        test_portfolio=portfolios[0],
        window_size=window_size,
        sample_number=sample_number,
        independent_windows=independent_windows,
        start_date=start_date,
        end_date=end_date,
        n_points=n_points,
    )

    return PortfolioReturnOptimizationResult(
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
