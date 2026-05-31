import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from .type import PortfolioReturnOptimizationResult


def plot_portfolio_return_optimization(results: PortfolioReturnOptimizationResult, title: str) -> None:
    if results.best_portfolio_region:
        fig = plt.figure(figsize=(20, 6))
        gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.5])
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        ax3 = fig.add_subplot(gs[2])
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    ranks = [p.rank for p in results.optimized_portfolios]
    scores = [p.portfolio_loss_score for p in results.optimized_portfolios]

    ax1.bar(ranks, scores, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Portfolio Rank', fontsize=12)
    ax1.set_ylabel('Return-Gap Loss Score', fontsize=12)
    ax1.set_title('Top Portfolios by Return-Gap Score', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.set_xticks(ranks)

    best_portfolio = results.best_portfolio
    asset_names = list(best_portfolio.weights.keys())
    weights = [best_portfolio.weights[name] for name in asset_names]

    colors = plt.cm.Set3(np.linspace(0, 1, len(asset_names)))
    wedges, texts, autotexts = ax2.pie(
        weights,
        labels=asset_names,
        autopct='%1.1f%%',
        colors=colors,
        startangle=90,
        textprops={'fontsize': 11}
    )

    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')

    ax2.set_title(f'Best Portfolio (Score: {best_portfolio.portfolio_loss_score:.4f})',
                  fontsize=13, fontweight='bold')

    if results.best_portfolio_region:
        region = results.best_portfolio_region
        num_windows = len(region.window_frontiers)
        frontier_colors = cm.tab20(np.linspace(0, 1, num_windows))

        for i, window_result in enumerate(region.window_frontiers):
            frontier = window_result.frontier
            label = f'W{i+1}: {window_result.start_date.date()}'

            ax3.plot(
                frontier['volatility'],
                frontier['annualized_return'],
                color=frontier_colors[i],
                linewidth=1.5,
                alpha=0.7,
                label=label
            )

        for i, window_result in enumerate(region.window_frontiers):
            test_point = window_result.test_portfolio_point
            ref_return = window_result.frontier_return_at_vol

            ax3.plot(
                [test_point.volatility, test_point.volatility],
                [test_point.annualized_return, ref_return],
                color=frontier_colors[i],
                linewidth=1.5,
                linestyle='--',
                alpha=0.5,
                zorder=5
            )

            ax3.scatter(
                test_point.volatility,
                test_point.annualized_return,
                s=120,
                color=frontier_colors[i],
                marker='o',
                zorder=10,
                edgecolors='black',
                linewidths=2
            )

        ax3.set_title('Return-Gap Region for Best Portfolio', fontsize=13, fontweight='bold')
        ax3.set_xlabel('Risk (Annualized Volatility %)', fontsize=11)
        ax3.set_ylabel('Return (Annualized %)', fontsize=11)
        ax3.set_xlim(left=0)
        ax3.grid(True, alpha=0.3)
        ax3.legend(loc='upper left', fontsize=8, framealpha=0.9)

    fig.suptitle(title, fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()


def print_results(results: PortfolioReturnOptimizationResult) -> None:
    print("=" * 80)
    print("PORTFOLIO RETURN OPTIMIZATION RESULTS")
    print("=" * 80)

    print(f"\nOptimization Configuration:")
    print(f"  Search Method:        {results.search_method}")
    print(f"  Portfolios Evaluated: {results.num_portfolios_evaluated}")
    print(f"  Analysis Period:      {results.requested_start_date.date()} to {results.requested_end_date.date()}")
    print(f"  Window Size:          {results.window_size} days")
    print(f"  Independent Windows:  {results.independent_windows}")

    print("\n" + "=" * 80)
    print("BEST PORTFOLIO")
    print("=" * 80)
    best = results.best_portfolio
    print(f"  Return-Gap Score: {best.portfolio_loss_score:.4f}")
    print(f"  Weights:")
    for asset, weight in sorted(best.weights.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            print(f"    {asset:20s} {weight:6.2f}%")

    print("\n" + "=" * 80)
    print(f"TOP {len(results.optimized_portfolios)} PORTFOLIOS")
    print("=" * 80)

    for portfolio in results.optimized_portfolios:
        print(f"\nRANK {portfolio.rank}")
        print("-" * 40)
        print(f"  Return-Gap Score: {portfolio.portfolio_loss_score:.4f}")
        print(f"  Weights:")
        for asset, weight in sorted(portfolio.weights.items(), key=lambda x: x[1], reverse=True):
            if weight > 0.01:
                print(f"    {asset:20s} {weight:6.2f}%")

    print("\n" + "=" * 80)
