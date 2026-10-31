from __future__ import annotations

from typing import Iterable, Optional

import pandas as pd

from src.analysis.comparative_analysis.analysis import compute_comparative_analysis
from src.analysis.correlation_matrix.analysis import compute_correlation_matrix
from src.analysis.discounted_analysis.analysis import compute_discounted_analysis
from src.analysis.drawdown.analysis import compute_drawdown
from src.analysis.efficient_frontier.analysis import compute_efficient_frontier
from src.analysis.rentability.analysis import compute_rentability
from src.analysis.risk_return_analysis.analysis import compute_risk_return_analysis
from src.analysis.rolling_comparison.analysis import compute_rolling_comparison
from src.analysis.sliding_window.analysis import compute_sliding_window
from src.consumers import IndexData
from src.consumers.consume import CONSUMERS, consume
from src.portfolio_generator.inflation_bonds_indexes import (
    INFLATION_BONDS_INDEXES,
    generate_inflation_bonds_portfolios,
    simulate_inflation_bonds_portfolio,
    simulate_inflation_bonds_portfolio_monthly,
)
from src.portfolio_generator.portfolio_simulator import (
    simulate_portfolio,
    simulate_portfolio_rebalanced,
    simulate_portfolio_rebalanced_monthly,
    simulate_portfolio_rebalanced_yearly,
)


class AnalysisApplication:
    """Orchestrate consumer data and the existing analysis functions.

    This is the application boundary used by the web API. It accepts consumer
    names rather than dataframes so clients cannot inject arbitrary portfolio
    data into this first version of the API.
    """

    @staticmethod
    def available_indexes() -> list[str]:
        return sorted(CONSUMERS)

    @staticmethod
    def get_index(index_name: str) -> IndexData:
        return consume(index_name)

    @classmethod
    def get_indexes(cls, index_names: Iterable[str]) -> list[IndexData]:
        names = list(index_names)
        if not names:
            raise ValueError("At least one index is required")

        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(f"Duplicate indexes are not allowed: {', '.join(duplicates)}")

        return [cls.get_index(name) for name in names]

    @staticmethod
    def _filter_dates(
        df: pd.DataFrame,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        filtered = df.copy()
        start = pd.to_datetime(start_date) if start_date is not None else None
        end = pd.to_datetime(end_date) if end_date is not None else None

        if start is not None and end is not None and start > end:
            raise ValueError("start_date must be before or equal to end_date")
        if start is not None:
            filtered = filtered[filtered["date"] >= start]
        if end is not None:
            filtered = filtered[filtered["date"] <= end]

        return filtered.sort_values("date").reset_index(drop=True)

    @classmethod
    def prices(
        cls,
        index_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> IndexData:
        index_data = cls.get_index(index_name)
        index_data["data"] = cls._filter_dates(index_data["data"], start_date, end_date)
        return index_data

    @classmethod
    def rentability(
        cls,
        index_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        index_data = cls.get_index(index_name)
        return compute_rentability(index_data["data"], start_date, end_date)

    @classmethod
    def drawdown(
        cls,
        index_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        index_data = cls.get_index(index_name)
        return compute_drawdown(index_data["data"], start_date, end_date)

    @classmethod
    def comparative(
        cls,
        index_names: Iterable[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        return compute_comparative_analysis(
            cls.get_indexes(index_names), start_date, end_date
        )

    @classmethod
    def correlation(
        cls,
        index_names: Iterable[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        interval: str = "daily",
    ):
        indexes = cls.get_indexes(index_names)
        return compute_correlation_matrix(
            [index_data["data"] for index_data in indexes],
            [index_data["name"] for index_data in indexes],
            start_date,
            end_date,
            interval,
        )

    @classmethod
    def discounted(
        cls,
        measured_index: str,
        reference_index: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        return compute_discounted_analysis(
            cls.get_index(measured_index),
            cls.get_index(reference_index),
            start_date,
            end_date,
        )

    @classmethod
    def risk_return(
        cls,
        index_names: Iterable[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        return compute_risk_return_analysis(cls.get_indexes(index_names), start_date, end_date)

    @classmethod
    def rolling_comparison(
        cls,
        index_a: str,
        index_b: str,
        window_years: float = 3.0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        return compute_rolling_comparison(
            cls.get_index(index_a),
            cls.get_index(index_b),
            window_years,
            start_date,
            end_date,
        )

    @classmethod
    def sliding_window(
        cls,
        index_names: Iterable[str],
        window_size: int,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        return compute_sliding_window(
            cls.get_indexes(index_names), window_size, start_date, end_date
        )

    @classmethod
    def risk_return_sliding_window(
        cls,
        index_names: Iterable[str],
        window_years: float,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        window_count: Optional[int] = None,
        independent_windows: bool = False,
    ):
        from src.analysis.risk_return_sliding_window.analysis import (
            compute_risk_return_sliding_window,
        )

        return compute_risk_return_sliding_window(
            cls.get_indexes(index_names),
            window_years,
            start_date,
            end_date,
            window_count,
            independent_windows,
        )

    @classmethod
    def efficient_frontier(
        cls,
        index_names: Iterable[str],
        risk_free_rate: float = 0.0,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        n_points: int = 200,
    ):
        return compute_efficient_frontier(
            cls.get_indexes(index_names),
            risk_free_rate,
            start_date,
            end_date,
            n_points,
        )

    @classmethod
    def portfolio_optimization(
        cls,
        index_names: Iterable[str],
        window_size: int,
        sample_number: int,
        independent_windows: bool = False,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        n_points: int = 200,
        step_size: int = 10,
        top_n: int = 10,
    ):
        from src.analysis.portfolio_optimization.analysis import optimize_portfolio

        return optimize_portfolio(
            cls.get_indexes(index_names),
            window_size,
            sample_number,
            independent_windows,
            start_date,
            end_date,
            n_points,
            step_size,
            top_n,
        )

    @classmethod
    def portfolio_return_optimization(
        cls,
        index_names: Iterable[str],
        window_size: int,
        sample_number: int,
        independent_windows: bool = False,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        n_points: int = 200,
        step_size: int = 10,
        top_n: int = 10,
    ):
        from src.analysis.portfolio_return_optimization.analysis import (
            optimize_portfolio_by_return,
        )

        return optimize_portfolio_by_return(
            cls.get_indexes(index_names),
            window_size,
            sample_number,
            independent_windows,
            start_date,
            end_date,
            n_points,
            step_size,
            top_n,
        )

    @classmethod
    def portfolio_testing(
        cls,
        components: Iterable[tuple[str, float]],
        rebalancing: str = "buy_and_hold",
        correlation_interval: str = "daily",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> dict:
        component_list = list(components)
        if not component_list:
            raise ValueError("At least one portfolio component is required")

        names = [name for name, _ in component_list]
        indexes = cls.get_indexes(names)
        weights = [float(weight) for _, weight in component_list]
        if any(weight < 0 for weight in weights):
            raise ValueError("Portfolio weights cannot be negative")
        if not any(weight > 0 for weight in weights):
            raise ValueError("At least one portfolio weight must be positive")

        total_weight = sum(weights)
        if abs(total_weight - 100.0) > 1e-6:
            raise ValueError(f"Portfolio weights must sum to 100%, got {total_weight:g}%")

        portfolio = [
            (index_data, weight / 100.0)
            for index_data, weight in zip(indexes, weights)
        ]
        simulators = {
            "buy_and_hold": simulate_portfolio,
            "daily": simulate_portfolio_rebalanced,
            "monthly": simulate_portfolio_rebalanced_monthly,
            "yearly": simulate_portfolio_rebalanced_yearly,
        }
        simulator = simulators.get(rebalancing)
        if simulator is None:
            available = ", ".join(simulators)
            raise ValueError(f"Unknown rebalancing '{rebalancing}'. Available: {available}")

        simulated = simulator(portfolio, start_date, end_date)
        simulated["name"] = "portfolio"
        all_series = [simulated, *indexes]

        return {
            "portfolio": simulated,
            "components": [
                {"index": name, "weight": weight}
                for name, weight in component_list
            ],
            "rebalancing": rebalancing,
            "rentability": compute_rentability(simulated["data"]),
            "drawdown": compute_drawdown(simulated["data"]),
            "risk_return": compute_risk_return_analysis(
                all_series, start_date, end_date
            ),
            "correlation": compute_correlation_matrix(
                [series["data"] for series in all_series],
                [series["name"] for series in all_series],
                start_date,
                end_date,
                correlation_interval,
            ),
        }

    @classmethod
    def inflation_bonds_risk_return(
        cls,
        random_portfolios: int = 40,
        seed: int = 42,
    ) -> dict:
        indexes = {
            name: cls.get_index(name) for name in INFLATION_BONDS_INDEXES
        }
        portfolios = generate_inflation_bonds_portfolios(
            indexes, random_portfolios=random_portfolios, seed=seed
        )

        monthly_portfolios = [
            simulate_inflation_bonds_portfolio_monthly(composition, name)
            for name, composition in portfolios
        ]
        buy_and_hold_portfolios = [
            simulate_inflation_bonds_portfolio(composition, f"Buy & Hold {name}")
            for name, composition in portfolios
        ]
        baseline_indexes = list(indexes.values())

        return {
            "monthly_rebalanced": compute_risk_return_analysis(
                baseline_indexes + monthly_portfolios
            ),
            "buy_and_hold": compute_risk_return_analysis(
                baseline_indexes + buy_and_hold_portfolios
            ),
            "generated_portfolios": len(portfolios),
        }
