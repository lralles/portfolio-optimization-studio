from typing import Optional, Dict
import pandas as pd

def compute_drawdown(df: pd.DataFrame, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
    filtered_df = df.copy()

    if start_date is not None:
        filtered_df = filtered_df[filtered_df['date'] >= pd.to_datetime(start_date)]
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['date'] <= pd.to_datetime(end_date)]

    filtered_df = filtered_df.reset_index(drop=True)

    cumulative_max = filtered_df['price'].cummax()
    drawdown = ((filtered_df['price'] - cumulative_max) / cumulative_max) * 100

    return {
        'filtered_df': filtered_df,
        'drawdown': pd.DataFrame({'date': filtered_df['date'], 'drawdown': drawdown}),
        'start_date': start_date,
        'end_date': end_date
    }
