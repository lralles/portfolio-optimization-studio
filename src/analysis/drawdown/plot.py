import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict

def plot_drawdown_from_results(results: Dict, title: str) -> None:
    df = results['filtered_df']
    drawdown_df = results['drawdown']

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(drawdown_df['date'], drawdown_df['drawdown'], linewidth=1)
    ax.fill_between(drawdown_df['date'], drawdown_df['drawdown'], 0, alpha=0.3)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Drawdown (%)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
