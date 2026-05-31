from dataclasses import dataclass
from typing import Dict, List
import pandas as pd

from ..efficient_region.type import PortfolioResult


@dataclass
class WindowReturnGapResult:
    window_index: int
    start_date: pd.Timestamp
    end_date: pd.Timestamp
    frontier: pd.DataFrame
    test_portfolio_point: PortfolioResult
    return_gap: float
    frontier_return_at_vol: float
    portfolio_error_score: float


@dataclass
class EfficientReturnRegionResult:
    window_frontiers: List[WindowReturnGapResult]
    assets: pd.DataFrame
    test_portfolio_weights: Dict[str, float]
    window_size: int
    sample_number: int
    independent_windows: bool
    requested_start_date: pd.Timestamp
    requested_end_date: pd.Timestamp
    num_windows: int
    portfolio_loss_score: float
