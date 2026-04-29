import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict

def plot_rentability(results: Dict, title: str) -> None:
    rentability_df = results['rentability']

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(rentability_df['date'], rentability_df['rentability'], linewidth=1)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Rentability (%)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
