import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict

def plot_discounted_analysis(results: Dict, title: str) -> None:
    aligned = results['aligned']
    measured_name = results['measured_name']
    reference_name = results['reference_name']

    measured_return = results['measured_return']
    reference_return = results['reference_return']
    discounted_return = results['discounted_return']

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(aligned['date'], measured_return, linewidth=1, label=f'{measured_name} return')
    ax.plot(aligned['date'], reference_return, linewidth=1, label=f'{reference_name} return')
    ax.plot(aligned['date'], discounted_return, linewidth=1.5, label=f'{measured_name} discounted by {reference_name}')

    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Return (%)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()
