from typing import List, Optional
import pandas as pd

from .type import RiskReturnAnalysisResult


def compute_risk_return_analysis(indexes: List[dict], start_date: Optional[str] = None, end_date: Optional[str] = None) -> RiskReturnAnalysisResult:
    dfs = {}
    for index_data in indexes:
        df = index_data['data'].sort_values('date').reset_index(drop=True)
        dfs[index_data['name']] = df

    if start_date is None:
        start_date = max(df['date'].iloc[0] for df in dfs.values())
    else:
        start_date = pd.to_datetime(start_date)
    
    if end_date is None:
        end_date = min(df['date'].iloc[-1] for df in dfs.values())
    else:
        end_date = pd.to_datetime(end_date)

    if start_date > end_date:
        return RiskReturnAnalysisResult(
            results_df=pd.DataFrame(columns=['index', 'annualized_return', 'annualized_volatility', 'total_return']),
            start_date=start_date,
            end_date=end_date,
        )

    results = []
    for name, df in dfs.items():
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered = df[mask].reset_index(drop=True)
        
        if len(filtered) < 2:
            continue
        
        initial_price = filtered['price'].iloc[0]
        rentability = ((filtered['price'] / initial_price) - 1) * 100
        
        total_return = rentability.iloc[-1]
        years = (filtered['date'].iloc[-1] - filtered['date'].iloc[0]).days / 365.25
        annualized_return = ((1 + total_return / 100) ** (1 / years) - 1) * 100
        
        returns = filtered['price'].pct_change().dropna()
        annualized_volatility = returns.std() * (252 ** 0.5) * 100
        
        results.append({
            'index': name,
            'annualized_return': annualized_return,
            'annualized_volatility': annualized_volatility,
            'total_return': total_return
        })

    results_df = pd.DataFrame(results)

    return RiskReturnAnalysisResult(
        results_df=results_df,
        start_date=start_date,
        end_date=end_date,
    )
