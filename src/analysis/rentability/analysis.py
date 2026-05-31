from typing import Optional
import pandas as pd

from .type import RentabilityResult


def compute_rentability(df: pd.DataFrame, start_date: Optional[str] = None, end_date: Optional[str] = None) -> RentabilityResult:
    filtered_df = df.copy()

    if start_date is not None:
        filtered_df = filtered_df[filtered_df['date'] >= pd.to_datetime(start_date)]
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['date'] <= pd.to_datetime(end_date)]

    filtered_df = filtered_df.reset_index(drop=True)

    initial_price = filtered_df['price'].iloc[0]
    rentability = ((filtered_df['price'] / initial_price) - 1) * 100

    total_return = rentability.iloc[-1]
    years = (filtered_df['date'].iloc[-1] - filtered_df['date'].iloc[0]).days / 365.25
    annualized_return = ((1 + total_return / 100) ** (1 / years) - 1) * 100

    returns = filtered_df['price'].pct_change().dropna()
    annualized_volatility = returns.std() * (252 ** 0.5) * 100

    return RentabilityResult(
        filtered_df=filtered_df,
        rentability=pd.DataFrame({'date': filtered_df['date'], 'rentability': rentability}),
        total_return=total_return,
        annualized_return=annualized_return,
        annualized_volatility=annualized_volatility,
        start_date=start_date,
        end_date=end_date,
    )
