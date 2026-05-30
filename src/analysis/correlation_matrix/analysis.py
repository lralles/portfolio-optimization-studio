from typing import List, Optional
import pandas as pd
from ..common_calculations.variations import get_day_variation, get_month_variation, get_year_variation
from .type import CorrelationMatrixResult


def compute_correlation_matrix(index_data_list: List[pd.DataFrame], index_names: List[str], start_date: Optional[str] = None, end_date: Optional[str] = None, interval: str = 'daily') -> CorrelationMatrixResult:
    if interval not in ['daily', 'month', 'year']:
        raise ValueError("interval must be 'daily', 'month', or 'year'")

    if len(index_data_list) != len(index_names):
        raise ValueError("index_data_list and index_names must have the same length")

    if interval == 'daily':
        variation_func = get_day_variation
    elif interval == 'month':
        variation_func = get_month_variation
    else:
        variation_func = get_year_variation

    variations_dict = {}
    for idx, (df, name) in enumerate(zip(index_data_list, index_names)):
        var_df = variation_func(df, start_date, end_date)
        variations_dict[name] = var_df.set_index('date')['variation']

    combined_df = pd.DataFrame(variations_dict)
    combined_df = combined_df.dropna()
    correlation_matrix = combined_df.corr()

    return CorrelationMatrixResult(
        combined_df=combined_df,
        correlation_matrix=correlation_matrix,
        start_date=start_date,
        end_date=end_date,
        interval=interval,
        index_names=index_names,
    )
