from typing import List, Optional, Dict
import pandas as pd

def compute_comparative_analysis(indexes: List[dict], start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
    dfs = {}
    for index_data in indexes:
        df = index_data['data'].sort_values('date').reset_index(drop=True)
        dfs[index_data['name']] = df

    common_start = max(df['date'].iloc[0] for df in dfs.values())
    common_end = min(df['date'].iloc[-1] for df in dfs.values())

    if start_date is not None:
        common_start = max(common_start, pd.to_datetime(start_date))
    if end_date is not None:
        common_end = min(common_end, pd.to_datetime(end_date))

    results = []
    rentability_timeseries = {}
    for name, df in dfs.items():
        mask = (df['date'] >= common_start) & (df['date'] <= common_end)
        filtered = df[mask].reset_index(drop=True)
        initial_price = filtered['price'].iloc[0]
        rentability = ((filtered['price'] / initial_price) - 1) * 100
        rentability_timeseries[name] = pd.DataFrame({'date': filtered['date'], 'rentability': rentability})

        total_return = rentability.iloc[-1]
        years = (filtered['date'].iloc[-1] - filtered['date'].iloc[0]).days / 365.25
        annualized_return = ((1 + total_return / 100) ** (1 / years) - 1) * 100

        results.append({
            'index': name,
            'total_return': total_return,
            'annualized_return': annualized_return
        })

    return {
        'results_df': pd.DataFrame(results),
        'rentability_timeseries': rentability_timeseries,
        'start_date': common_start,
        'end_date': common_end
    }
