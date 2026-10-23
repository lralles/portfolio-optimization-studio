from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from src.consumers import IndexData


INFLATION_BONDS_INDEXES = (
    "imab",
    "imab5",
    "imab5mais",
    "idkaipca2",
    "idkaipca3",
    "idkaipca5",
    "idkaipca10",
    "idkaipca15",
    "idkaipca20",
    "idkaipca30",
)


def _composition(indexes: Dict[str, IndexData], weights: Dict[str, float]) -> List[Tuple[IndexData, float]]:
    missing = set(weights) - set(indexes)
    if missing:
        raise ValueError(f"Missing indexes: {', '.join(sorted(missing))}")

    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Portfolio weights must have a positive sum")

    return [(indexes[name], weight / total) for name, weight in weights.items() if weight > 0]


def _profile_weights(profile: str, rng: np.random.Generator) -> Dict[str, float]:
    maturities = np.array([2, 3, 5, 10, 15, 20, 30], dtype=float)
    ipca_names = [f"idkaipca{years}" for years in maturities.astype(int)]

    if profile == "short":
        # More exposure to short duration, while retaining every requested asset.
        alpha = np.exp(-maturities / 5) * 3.0 + 0.15
    elif profile == "long":
        alpha = np.exp(maturities / 14) * 0.9 + 0.15
    else:
        alpha = np.ones(len(maturities)) * 1.1

    ipca_weights = rng.dirichlet(alpha)
    imab_weights = rng.dirichlet(np.array([1.5, 1.5, 1.5]))
    weights = {
        "imab": float(imab_weights[0] * 0.30),
        "imab5": float(imab_weights[1] * 0.30),
        "imab5mais": float(imab_weights[2] * 0.30),
    }
    weights.update({name: float(weight * 0.70) for name, weight in zip(ipca_names, ipca_weights)})
    return weights


def generate_inflation_bonds_portfolios(
    indexes: Dict[str, IndexData],
    random_portfolios: int = 120,
    seed: int = 42,
) -> List[Tuple[str, List[Tuple[IndexData, float]]]]:
    """Create named short-, medium-, long-term, and randomized inflation-bond portfolios."""
    required = set(INFLATION_BONDS_INDEXES)
    missing = required - set(indexes)
    if missing:
        raise ValueError(f"Missing indexes: {', '.join(sorted(missing))}")
    if random_portfolios < 0:
        raise ValueError("random_portfolios must be non-negative")

    rng = np.random.default_rng(seed)
    portfolios: List[Tuple[str, List[Tuple[IndexData, float]]]] = []

    for profile in ("short", "medium", "long"):
        for number in range(1, 5):
            portfolios.append((
                f"{profile.title()} profile {number}",
                _composition(indexes, _profile_weights(profile, rng)),
            ))

    for number in range(1, random_portfolios + 1):
        profile = ("short", "medium", "long")[number % 3]
        portfolios.append((
            f"Random {profile} {number:03d}",
            _composition(indexes, _profile_weights(profile, rng)),
        ))

    return portfolios


def simulate_inflation_bonds_portfolio_monthly(
    portfolio: List[Tuple[IndexData, float]],
    name: str,
) -> IndexData:
    """Simulate a monthly-rebalanced portfolio using aligned vector operations."""
    if not portfolio:
        raise ValueError("Portfolio cannot be empty")

    weights = {index_data["name"]: weight for index_data, weight in portfolio}
    if abs(sum(weights.values()) - 1.0) > 1e-6:
        raise ValueError("Weights must sum to 1.0")

    prices = []
    for index_data, _ in portfolio:
        series = index_data["data"][["date", "price"]].copy()
        series = series.rename(columns={"price": index_data["name"]}).set_index("date")
        prices.append(series)

    aligned = pd.concat(prices, axis=1, join="inner").sort_index()
    if aligned.empty:
        raise ValueError("No common dates found across all indexes")

    returns = aligned.pct_change().fillna(0.0)
    target_weights = pd.Series(weights, dtype=float)
    values = []
    portfolio_value = 1.0
    current_weights = target_weights.copy()
    previous_month = None

    for date, daily_returns in returns.iterrows():
        month = (date.year, date.month)
        if month != previous_month:
            current_weights = target_weights.copy()
            previous_month = month

        portfolio_return = float((daily_returns * current_weights).sum())
        portfolio_value *= 1.0 + portfolio_return
        values.append({"date": date, "price": portfolio_value})

        asset_values = current_weights * (1.0 + daily_returns)
        current_weights = asset_values / (1.0 + portfolio_return)

    return IndexData(name=name, data=pd.DataFrame(values))


def simulate_inflation_bonds_portfolio(
    portfolio: List[Tuple[IndexData, float]],
    name: str,
) -> IndexData:
    """Simulate a buy-and-hold portfolio without rebalancing."""
    if not portfolio:
        raise ValueError("Portfolio cannot be empty")

    weights = {index_data["name"]: weight for index_data, weight in portfolio}
    if abs(sum(weights.values()) - 1.0) > 1e-6:
        raise ValueError("Weights must sum to 1.0")

    prices = []
    for index_data, _ in portfolio:
        series = index_data["data"][["date", "price"]].copy()
        series = series.rename(columns={"price": index_data["name"]}).set_index("date")
        prices.append(series)

    aligned = pd.concat(prices, axis=1, join="inner").sort_index()
    if aligned.empty:
        raise ValueError("No common dates found across all indexes")

    returns = aligned.pct_change().fillna(0.0)
    current_weights = pd.Series(weights, dtype=float)
    values = []
    portfolio_value = 1.0

    for date, daily_returns in returns.iterrows():
        portfolio_return = float((daily_returns * current_weights).sum())
        portfolio_value *= 1.0 + portfolio_return
        values.append({"date": date, "price": portfolio_value})

        asset_values = current_weights * (1.0 + daily_returns)
        current_weights = asset_values / (1.0 + portfolio_return)

    return IndexData(name=name, data=pd.DataFrame(values))
