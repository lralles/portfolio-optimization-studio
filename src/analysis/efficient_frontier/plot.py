import matplotlib.pyplot as plt
from typing import Optional

from .type import EfficientFrontierResult
from ..risk_return_analysis.type import RiskReturnAnalysisResult


def plot_efficient_frontier(results: EfficientFrontierResult, title: str, risk_return_results: Optional[RiskReturnAnalysisResult] = None) -> None:
    frontier = results.frontier
    assets = results.assets
    min_var = results.min_variance_portfolio
    max_ret = results.max_return_portfolio
    tangency = results.tangency_portfolio
    rf = results.risk_free_rate

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(frontier['volatility'], frontier['annualized_return'], color='steelblue', linewidth=2, zorder=2, label='Efficient Frontier')

    ax.scatter(assets['volatility'], assets['annualized_return'], s=80, color='gray', alpha=0.7, zorder=3, label='Assets')
    for _, row in assets.iterrows():
        ax.annotate(row['name'], (row['volatility'], row['annualized_return']), xytext=(5, 5), textcoords='offset points', fontsize=9, color='gray')

    ax.scatter(min_var.volatility, min_var.annualized_return, s=150, color='green', zorder=5, marker='*', label='Min Variance')
    ax.annotate('Min Variance', (min_var.volatility, min_var.annualized_return), xytext=(8, -12), textcoords='offset points', fontsize=9, color='green', fontweight='bold')

    ax.scatter(max_ret.volatility, max_ret.annualized_return, s=150, color='red', zorder=5, marker='*', label='Max Return')
    ax.annotate('Max Return', (max_ret.volatility, max_ret.annualized_return), xytext=(8, 5), textcoords='offset points', fontsize=9, color='red', fontweight='bold')

    ax.scatter(tangency.volatility, tangency.annualized_return, s=150, color='orange', zorder=5, marker='*', label=f'Tangency (rf={rf:.1f}%)')
    ax.annotate(f'Tangency', (tangency.volatility, tangency.annualized_return), xytext=(8, 5), textcoords='offset points', fontsize=9, color='orange', fontweight='bold')

    selected_vols = [p.volatility for p in results.selected_portfolios]
    selected_rets = [p.annualized_return for p in results.selected_portfolios]
    ax.scatter(selected_vols, selected_rets, s=100, color='blue', zorder=4, marker='o', alpha=0.6, label='Selected Portfolios')

    vol_range_end = max(frontier['volatility'].max(), assets['volatility'].max()) * 1.1
    cml_vol = [0, vol_range_end]
    slope = (tangency.annualized_return - rf) / tangency.volatility
    cml_ret = [rf, rf + slope * vol_range_end]
    ax.plot(cml_vol, cml_ret, linestyle='--', color='orange', linewidth=1.2, alpha=0.7, label='Capital Market Line')

    if risk_return_results is not None:
        rr_df = risk_return_results.results_df
        ax.scatter(rr_df['annualized_volatility'], rr_df['annualized_return'], s=100, color='purple', alpha=0.8, zorder=4, marker='D', label='Sample Portfolios')
        for _, row in rr_df.iterrows():
            ax.annotate(row['index'], (row['annualized_volatility'], row['annualized_return']), xytext=(5, 5), textcoords='offset points', fontsize=9, color='purple')

    ax.set_title(title)
    ax.set_xlabel('Risk (Annualized Volatility %)')
    ax.set_ylabel('Return (Annualized %)')
    ax.set_xlim(left=0)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    plt.tight_layout()
    plt.show()


def print_results(results: EfficientFrontierResult) -> None:
    print("=" * 80)
    print("EFFICIENT FRONTIER ANALYSIS RESULTS")
    print("=" * 80)
    
    print(f"\nAnalysis Period:")
    print(f"  Requested:  {results.start_date} to {results.end_date}")
    print(f"  Effective:  {results.effective_start_date} to {results.effective_end_date}")
    print(f"  Common dates: {results.num_common_dates}")
    print(f"  Risk-free rate: {results.risk_free_rate:.2f}%")
    
    print("\n" + "=" * 80)
    print("INDIVIDUAL ASSETS")
    print("=" * 80)
    assets = results.assets
    for _, asset in assets.iterrows():
        print(f"\n{asset['name']}:")
        print(f"  Return:     {asset['annualized_return']:8.2f}%")
        print(f"  Volatility: {asset['volatility']:8.2f}%")
        print(f"  Variance:   {asset['variance']:8.2f}%²")
    
    print("\n" + "=" * 80)
    print("OPTIMAL PORTFOLIOS")
    print("=" * 80)
    
    print("\nMINIMUM VARIANCE PORTFOLIO")
    print("-" * 40)
    min_var = results.min_variance_portfolio
    print(f"  Return:     {min_var.annualized_return:8.2f}%")
    print(f"  Volatility: {min_var.volatility:8.2f}%")
    print(f"  Variance:   {min_var.variance:8.2f}%²")
    print(f"  Weights:")
    for asset, weight in sorted(min_var.weights.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            print(f"    {asset:20s} {weight:6.2f}%")
    
    print("\nTANGENCY PORTFOLIO (Maximum Sharpe Ratio)")
    print("-" * 40)
    tangency = results.tangency_portfolio
    sharpe = (tangency.annualized_return - results.risk_free_rate) / tangency.volatility
    print(f"  Return:     {tangency.annualized_return:8.2f}%")
    print(f"  Volatility: {tangency.volatility:8.2f}%")
    print(f"  Variance:   {tangency.variance:8.2f}%²")
    print(f"  Sharpe:     {sharpe:8.4f}")
    print(f"  Weights:")
    for asset, weight in sorted(tangency.weights.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            print(f"    {asset:20s} {weight:6.2f}%")
    
    print("\nMAXIMUM RETURN PORTFOLIO")
    print("-" * 40)
    max_ret = results.max_return_portfolio
    print(f"  Return:     {max_ret.annualized_return:8.2f}%")
    print(f"  Volatility: {max_ret.volatility:8.2f}%")
    print(f"  Variance:   {max_ret.variance:8.2f}%²")
    print(f"  Weights:")
    for asset, weight in sorted(max_ret.weights.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            print(f"    {asset:20s} {weight:6.2f}%")
    
    print("\n" + "=" * 80)
    print("SELECTED EFFICIENT FRONTIER PORTFOLIOS (10 EVENLY SPACED)")
    print("=" * 80)
    
    for i, portfolio in enumerate(results.selected_portfolios, 1):
        print(f"\nPORTFOLIO {i}")
        print("-" * 40)
        print(f"  Return:     {portfolio.annualized_return:8.2f}%")
        print(f"  Volatility: {portfolio.volatility:8.2f}%")
        print(f"  Variance:   {portfolio.variance:8.2f}%²")
        print(f"  Weights:")
        for asset, weight in sorted(portfolio.weights.items(), key=lambda x: x[1], reverse=True):
            if weight > 0.01:
                print(f"    {asset:20s} {weight:6.2f}%")
    
    print("\n" + "=" * 80)
