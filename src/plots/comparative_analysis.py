import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

def plot_comparative_analysis(indexes, title):
    dfs = {}
    for name in indexes:
        df = pd.read_csv(Path('sanitized_data') / f'{name}.csv', parse_dates=['date'])
        dfs[name] = df.sort_values('date').reset_index(drop=True)

    start_date = max(df['date'].iloc[0] for df in dfs.values())
    end_date = min(df['date'].iloc[-1] for df in dfs.values())

    fig, ax = plt.subplots(figsize=(14, 5))

    for name, df in dfs.items():
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filtered = df[mask].reset_index(drop=True)
        initial_price = filtered['price'].iloc[0]
        rentability = ((filtered['price'] / initial_price) - 1) * 100
        ax.plot(filtered['date'], rentability, linewidth=1, label=name)

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
