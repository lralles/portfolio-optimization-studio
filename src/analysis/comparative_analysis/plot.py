import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from .type import ComparativeAnalysisResult


def plot_comparative_analysis(results: ComparativeAnalysisResult, title: str) -> None:
    fig, ax = plt.subplots(figsize=(14, 5))

    for name, df in results.rentability_timeseries.items():
        ax.plot(df['date'], df['rentability'], linewidth=1, label=name)

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
