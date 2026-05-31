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
class WindowFrontierResult:
    window_index: int
    start_date: pd.Timestamp
    end_date: pd.Timestamp
    frontier: pd.DataFrame
    test_portfolio_point: PortfolioResult
    distance_to_frontier: float
    closest_frontier_point: tuple


@dataclass
class EfficientRegionResult:
    window_frontiers: List[WindowFrontierResult]
    assets: pd.DataFrame
    test_portfolio_weights: Dict[str, float]
    window_size: int
    sample_number: int
    independent_windows: bool
    requested_start_date: pd.Timestamp
    requested_end_date: pd.Timestamp
    num_windows: int
    portfolio_loss_score: float
