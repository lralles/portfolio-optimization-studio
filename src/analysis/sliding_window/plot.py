import matplotlib.pyplot as plt
from typing import Dict


def plot_sliding_window(results: Dict, title: str) -> None:
    data = results['results']
    window_size = results['window_size']

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    for name, df in data.items():
        ax1.plot(df['date'], df['annualized_return'], linewidth=1.5, label=name)

    ax1.set_title(f'{title} — Annualized Return ({window_size}-day window)')
    ax1.set_ylabel('Annualized Return (%)')
    ax1.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')

    for name, df in data.items():
        ax2.plot(df['date'], df['annualized_volatility'], linewidth=1.5, label=name)

    ax2.set_title(f'Annualized Volatility ({window_size}-day window)')
    ax2.set_ylabel('Annualized Volatility (%)')
    ax2.set_xlabel('Date')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper left')

    plt.tight_layout()
    plt.show()
