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
