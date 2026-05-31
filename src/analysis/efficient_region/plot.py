import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

from .type import EfficientRegionResult


def plot_efficient_region(results: EfficientRegionResult, title: str) -> None:
    fig, ax = plt.subplots(figsize=(14, 10))

    num_windows = len(results.window_frontiers)
    colors = cm.tab20(np.linspace(0, 1, num_windows))

    for i, window_result in enumerate(results.window_frontiers):
        frontier = window_result.frontier
        label = f'Window {i+1}: {window_result.start_date.date()} to {window_result.end_date.date()}'
        
        ax.plot(
            frontier['volatility'], 
            frontier['annualized_return'], 
            color=colors[i], 
            linewidth=1.5, 
            alpha=0.7,
            label=label
        )

    for i, window_result in enumerate(results.window_frontiers):
        test_point = window_result.test_portfolio_point
        closest_point = window_result.closest_frontier_point
        
        ax.plot(
            [test_point.volatility, closest_point[0]],
            [test_point.annualized_return, closest_point[1]],
            color=colors[i],
            linewidth=1.5,
            linestyle='--',
            alpha=0.5,
            zorder=5
        )
        
        ax.scatter(
            test_point.volatility, 
            test_point.annualized_return, 
            s=150, 
            color=colors[i], 
            marker='o', 
            zorder=10,
            edgecolors='black',
            linewidths=2
        )

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Risk (Annualized Volatility %)', fontsize=12)
    ax.set_ylabel('Return (Annualized %)', fontsize=12)
    ax.set_xlim(left=0)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.9)
    
    plt.tight_layout()
    plt.show()


def print_results(results: EfficientRegionResult) -> None:
    print("=" * 80)
    print("EFFICIENT REGION ANALYSIS RESULTS")
    print("=" * 80)
    
    print(f"\nAnalysis Configuration:")
    print(f"  Requested Period:     {results.requested_start_date.date()} to {results.requested_end_date.date()}")
    print(f"  Window Size:          {results.window_size} days")
    print(f"  Independent Windows:  {results.independent_windows}")
    print(f"  Number of Windows:    {results.num_windows}")
    
    print("\n" + "=" * 80)
    print("TEST PORTFOLIO WEIGHTS")
    print("=" * 80)
    for asset, weight in sorted(results.test_portfolio_weights.items(), key=lambda x: x[1], reverse=True):
        if weight > 0.01:
            print(f"  {asset:20s} {weight:6.2f}%")
    
    print("\n" + "=" * 80)
    print("PORTFOLIO LOSS SCORE")
    print("=" * 80)
    print(f"  Average Error Score (normalized): {results.portfolio_loss_score:.4f}")
    
    print("\n" + "=" * 80)
    print("WINDOW ANALYSIS")
    print("=" * 80)
    
    for window_result in results.window_frontiers:
        print(f"\nWINDOW {window_result.window_index + 1}")
        print("-" * 40)
        print(f"  Period: {window_result.start_date.date()} to {window_result.end_date.date()}")
        print(f"  Test Portfolio Performance:")
        print(f"    Return:     {window_result.test_portfolio_point.annualized_return:8.2f}%")
        print(f"    Volatility: {window_result.test_portfolio_point.volatility:8.2f}%")
        print(f"    Variance:   {window_result.test_portfolio_point.variance:8.2f}%²")
        print(f"  Distance to Frontier:        {window_result.distance_to_frontier:.4f}")
        print(f"  Portfolio Error Score:        {window_result.portfolio_error_score:.4f}")
    
    print("\n" + "=" * 80)
