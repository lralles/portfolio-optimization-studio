import matplotlib.pyplot as plt
from typing import Dict


def plot_efficient_frontier(results: Dict, title: str) -> None:
    frontier = results['frontier']
    assets = results['assets']
    min_var = results['min_variance_portfolio']
    max_ret = results['max_return_portfolio']
    tangency = results['tangency_portfolio']
    rf = results['risk_free_rate']

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(frontier['volatility'], frontier['annualized_return'], color='steelblue', linewidth=2, zorder=2, label='Efficient Frontier')

    ax.scatter(assets['volatility'], assets['annualized_return'], s=80, color='gray', alpha=0.7, zorder=3, label='Assets')
    for _, row in assets.iterrows():
        ax.annotate(row['name'], (row['volatility'], row['annualized_return']), xytext=(5, 5), textcoords='offset points', fontsize=9, color='gray')

    ax.scatter(min_var['volatility'], min_var['annualized_return'], s=150, color='green', zorder=5, marker='*', label='Min Variance')
    ax.annotate('Min Variance', (min_var['volatility'], min_var['annualized_return']), xytext=(8, -12), textcoords='offset points', fontsize=9, color='green', fontweight='bold')

    ax.scatter(max_ret['volatility'], max_ret['annualized_return'], s=150, color='red', zorder=5, marker='*', label='Max Return')
    ax.annotate('Max Return', (max_ret['volatility'], max_ret['annualized_return']), xytext=(8, 5), textcoords='offset points', fontsize=9, color='red', fontweight='bold')

    ax.scatter(tangency['volatility'], tangency['annualized_return'], s=150, color='orange', zorder=5, marker='*', label=f'Tangency (rf={rf:.1f}%)')
    ax.annotate(f'Tangency', (tangency['volatility'], tangency['annualized_return']), xytext=(8, 5), textcoords='offset points', fontsize=9, color='orange', fontweight='bold')

    vol_range_end = max(frontier['volatility'].max(), assets['volatility'].max()) * 1.1
    cml_vol = [0, vol_range_end]
    slope = (tangency['annualized_return'] - rf) / tangency['volatility']
    cml_ret = [rf, rf + slope * vol_range_end]
    ax.plot(cml_vol, cml_ret, linestyle='--', color='orange', linewidth=1.2, alpha=0.7, label='Capital Market Line')

    ax.set_title(title)
    ax.set_xlabel('Risk (Annualized Volatility %)')
    ax.set_ylabel('Return (Annualized %)')
    ax.set_xlim(left=0)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right')
    plt.tight_layout()
    plt.show()
