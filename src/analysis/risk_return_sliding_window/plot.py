import matplotlib.pyplot as plt

from .type import RiskReturnSlidingWindowResult


def plot_risk_return_sliding_window(results: RiskReturnSlidingWindowResult, title: str) -> None:
    fig, ax = plt.subplots(figsize=(12, 8))

    for name, df in results.results.items():
        if len(df) == 0:
            continue

        ax.plot(
            df['annualized_volatility'],
            df['annualized_return'],
            linewidth=1.5,
            alpha=0.8,
            label=name,
        )
        ax.scatter(
            df['annualized_volatility'],
            df['annualized_return'],
            s=20,
            alpha=0.6,
        )

        first = df.iloc[0]
        last = df.iloc[-1]
        ax.annotate(f"{name} start", (first['annualized_volatility'], first['annualized_return']), xytext=(5, 5), textcoords='offset points', fontsize=8)
        ax.annotate(f"{name} end", (last['annualized_volatility'], last['annualized_return']), xytext=(5, -10), textcoords='offset points', fontsize=8)

    ax.set_title(f"{title} ({results.window_years:.4g}-year sliding window)")
    ax.set_xlabel('Risk (Annualized Volatility %)')
    ax.set_ylabel('Return (Annualized %)')
    ax.set_xlim(left=0)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    plt.tight_layout()
    plt.show()
