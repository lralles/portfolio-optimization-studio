import matplotlib.pyplot as plt
from typing import Dict


def plot_rolling_comparison(results: Dict, title: str) -> None:
    diff = results['difference']
    name_a = results['name_a']
    name_b = results['name_b']
    window_years = results['window_years']

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(diff['date'], diff['difference'], color='steelblue', linewidth=1.5, label=f'{name_a} − {name_b}')

    ax.fill_between(diff['date'], diff['difference'], 0,
                    where=diff['difference'] >= 0, alpha=0.25, color='green', label=f'{name_a} outperforming')
    ax.fill_between(diff['date'], diff['difference'], 0,
                    where=diff['difference'] < 0, alpha=0.25, color='red', label=f'{name_b} outperforming')

    ax.axhline(0, color='black', linewidth=1.2, linestyle='--', alpha=0.7)

    ax.set_title(f'{title} ({window_years:.4g}-year rolling window)')
    ax.set_xlabel('Date')
    ax.set_ylabel(f'Return Difference (% annualized)  [{name_a} − {name_b}]')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    plt.tight_layout()
    plt.show()


def print_results(results: Dict) -> None:
    name_a = results['name_a']
    name_b = results['name_b']
    window_years = results['window_years']
    total = results['total_windows']
    wins_a = results['wins_a']
    wins_b = results['wins_b']
    win_pct_a = results['win_pct_a']
    win_pct_b = results['win_pct_b']
    diff = results['difference']

    print("=" * 60)
    print("ROLLING COMPARISON RESULTS")
    print("=" * 60)
    print(f"\n  {name_a}  vs  {name_b}")
    print(f"  Window:        {window_years:.4g} year(s)")
    print(f"  Period:        {results['start_date'].date()} to {results['end_date'].date()}")
    print(f"  Total windows: {total}")

    print(f"\n  {'':20} {'Windows won':>12} {'Win rate':>10} {'Avg margin':>12}")
    print("  " + "-" * 56)
    avg_when_a = diff.loc[diff['difference'] > 0, 'difference'].mean()
    avg_when_b = diff.loc[diff['difference'] < 0, 'difference'].abs().mean()
    print(f"  {name_a:<20} {wins_a:>12} {win_pct_a:>9.1f}% {avg_when_a:>+11.2f}%")
    print(f"  {name_b:<20} {wins_b:>12} {win_pct_b:>9.1f}% {avg_when_b:>+11.2f}%")

    print(f"\n  Max outperformance ({name_a}): {diff['difference'].max():+.2f}%")
    print(f"  Max outperformance ({name_b}): {diff['difference'].min():+.2f}%")
    print(f"  Avg difference (a - b):       {diff['difference'].mean():+.2f}%")
    print("=" * 60)
