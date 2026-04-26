import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_risk_return_analysis(indexes, title, start_date=None, end_date=None):
    dfs = {}
    for name in indexes:
        df = pd.read_csv(Path('sanitized_data') / f'{name}.csv', parse_dates=['date'])
        dfs[name] = df.sort_values('date').reset_index(drop=True)

    if start_date is None:
        start_date = max(df['date'].iloc[0] for df in dfs.values())
    else:
        start_date = pd.to_datetime(start_date)
    
    if end_date is None:
        end_date = min(df['date'].iloc[-1] for df in dfs.values())
    else:
        end_date = pd.to_datetime(end_date)
    
    if start_date > end_date:
        print(f"Error: No overlapping date range found across all indexes.")
        print(f"Latest start date: {start_date}, Earliest end date: {end_date}")
        return pd.DataFrame(columns=['index', 'annualized_return', 'annualized_volatility', 'total_return'])

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

    if len(results) == 0:
        print(f"No data available for the specified date range: {start_date} to {end_date}")
        return pd.DataFrame(columns=['index', 'annualized_return', 'annualized_volatility', 'total_return'])
    
    results_df = pd.DataFrame(results)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.scatter(results_df['annualized_volatility'], results_df['annualized_return'], 
               s=100, alpha=0.6)
    
    for idx, row in results_df.iterrows():
        ax.annotate(row['index'], 
                   (row['annualized_volatility'], row['annualized_return']),
                   xytext=(5, 5), textcoords='offset points', fontsize=9)
    
    ax.set_title(title)
    ax.set_xlabel('Risk (Annualized Volatility %)')
    ax.set_ylabel('Return (Annualized %)')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    return results_df[['index', 'annualized_return', 'annualized_volatility', 'total_return']]
