import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

def get_and_plot_comparative_analysis(indexes, title):
    dfs = {}
    for name in indexes:
        df = pd.read_csv(Path('sanitized_data') / f'{name}.csv', parse_dates=['date'])
        dfs[name] = df.sort_values('date').reset_index(drop=True)

    start_date = max(df['date'].iloc[0] for df in dfs.values())
    end_date = min(df['date'].iloc[-1] for df in dfs.values())

    fig, ax = plt.subplots(figsize=(14, 5))
    
    results = []
    for name, df in dfs.items():
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered = df[mask].reset_index(drop=True)
        initial_price = filtered['price'].iloc[0]
        rentability = ((filtered['price'] / initial_price) - 1) * 100
        ax.plot(filtered['date'], rentability, linewidth=1, label=name)
        
        total_return = rentability.iloc[-1]
        years = (filtered['date'].iloc[-1] - filtered['date'].iloc[0]).days / 365.25
        annualized_return = ((1 + total_return / 100) ** (1 / years) - 1) * 100
        
        results.append({
            'index': name,
            'total_return': total_return,
            'annualized_return': annualized_return
        })

    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Rentability (%)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()
    
    return pd.DataFrame(results)
