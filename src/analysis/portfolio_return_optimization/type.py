from dataclasses import dataclass
from typing import Dict, List, Optional
import pandas as pd

from ..efficient_return_region.type import EfficientReturnRegionResult


@dataclass
class OptimizedPortfolioResult:
    weights: Dict[str, float]
    portfolio_loss_score: float
    rank: int


@dataclass
class PortfolioReturnOptimizationResult:
    optimized_portfolios: List[OptimizedPortfolioResult]
    best_portfolio: OptimizedPortfolioResult
    best_portfolio_region: Optional[EfficientReturnRegionResult]
    search_method: str
    num_portfolios_evaluated: int
    window_size: int
    sample_number: int
    independent_windows: bool
    requested_start_date: pd.Timestamp
    requested_end_date: pd.Timestamp
