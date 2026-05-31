from dataclasses import dataclass
from typing import Dict, List
import pandas as pd


@dataclass
class PortfolioResult:
    weights: Dict[str, float]
    annualized_return: float
    volatility: float
    variance: float


@dataclass
class EfficientFrontierResult:
    frontier: pd.DataFrame
    assets: pd.DataFrame
    min_variance_portfolio: PortfolioResult
    max_return_portfolio: PortfolioResult
    tangency_portfolio: PortfolioResult
    selected_portfolios: List[PortfolioResult]
    risk_free_rate: float
    start_date: pd.Timestamp
    end_date: pd.Timestamp
    effective_start_date: pd.Timestamp
    effective_end_date: pd.Timestamp
    num_common_dates: int


def print_results(result: EfficientFrontierResult) -> None:
    print("=" * 80)
    print("EFFICIENT FRONTIER ANALYSIS RESULTS")
    print("=" * 80)
    print(f"Requested: {result.start_date.date()} to {result.end_date.date()}")
    print(f"Effective: {result.effective_start_date.date()} to {result.effective_end_date.date()}")
    print(f"Common dates: {result.num_common_dates}")
    print(f"Risk-free rate: {result.risk_free_rate:.2f}%")
    print("\nAssets:")
    print(result.assets[['name', 'annualized_return', 'volatility']].to_string(index=False))
    print("\nMin Variance:")
    print(f"Return: {result.min_variance_portfolio.annualized_return:.2f}%")
    print(f"Volatility: {result.min_variance_portfolio.volatility:.2f}%")
    print("\nTangency:")
    print(f"Return: {result.tangency_portfolio.annualized_return:.2f}%")
    print(f"Volatility: {result.tangency_portfolio.volatility:.2f}%")
    print("\nMax Return:")
    print(f"Return: {result.max_return_portfolio.annualized_return:.2f}%")
    print(f"Volatility: {result.max_return_portfolio.volatility:.2f}%")
