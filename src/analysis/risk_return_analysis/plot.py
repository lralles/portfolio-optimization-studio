import matplotlib.pyplot as plt

from .type import RiskReturnAnalysisResult


def plot_risk_return(results: RiskReturnAnalysisResult, title: str) -> None:
    results_df = results.results_df

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(results_df['annualized_volatility'], results_df['annualized_return'], s=100, alpha=0.6)

    for idx, row in results_df.iterrows():
        ax.annotate(row['index'], (row['annualized_volatility'], row['annualized_return']), xytext=(5, 5), textcoords='offset points', fontsize=9)

    ax.set_title(title)
    ax.set_xlabel('Risk (Annualized Volatility %)')
    ax.set_ylabel('Return (Annualized %)')
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_portfolio_risk_return(results: RiskReturnAnalysisResult, title: str) -> None:
    """Plot every portfolio; annotate only the named profile portfolios."""
    results_df = results.results_df
    fig, ax = plt.subplots(figsize=(13, 8))

    random_mask = results_df['index'].str.startswith('Random ')
    profile_mask = results_df['index'].str.match(r'^(Short|Medium|Long) profile ')
    buy_hold_mask = results_df['index'].str.startswith('Buy & Hold ')
    baseline_mask = ~random_mask & ~profile_mask & ~buy_hold_mask
    ax.scatter(
        results_df.loc[random_mask, 'annualized_volatility'],
        results_df.loc[random_mask, 'annualized_return'],
        s=28,
        alpha=0.45,
        label='Random mixes',
    )
    profile_df = results_df.loc[profile_mask]
    ax.scatter(
        profile_df['annualized_volatility'],
        profile_df['annualized_return'],
        s=75,
        alpha=0.9,
        label='Term profiles',
    )

    buy_hold_df = results_df.loc[buy_hold_mask]
    ax.scatter(
        buy_hold_df['annualized_volatility'],
        buy_hold_df['annualized_return'],
        s=42,
        alpha=0.55,
        label='Buy-and-hold mixes',
    )

    baseline_df = results_df.loc[baseline_mask]
    ax.scatter(
        baseline_df['annualized_volatility'],
        baseline_df['annualized_return'],
        s=95,
        marker='D',
        alpha=0.95,
        label='Baseline indexes',
    )

    for _, row in profile_df.iterrows():
        ax.annotate(row['index'], (row['annualized_volatility'], row['annualized_return']),
                    xytext=(4, 4), textcoords='offset points', fontsize=8)

    for _, row in baseline_df.iterrows():
        ax.annotate(row['index'], (row['annualized_volatility'], row['annualized_return']),
                    xytext=(4, -10), textcoords='offset points', fontsize=8)

    ax.set_title(title)
    ax.set_xlabel('Risk (Annualized Volatility %)')
    ax.set_ylabel('Return (Annualized %)')
    ax.set_xlim(left=0)
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()
