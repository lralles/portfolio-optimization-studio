import matplotlib.pyplot as plt
import numpy as np

from .type import CorrelationMatrixResult


def plot_correlation_matrix(results: CorrelationMatrixResult) -> None:
    index_names = results.index_names
    correlation_matrix = results.correlation_matrix
    start_date = results.start_date
    end_date = results.end_date
    interval = results.interval

    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
    cbar = plt.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label('Correlation', rotation=270, labelpad=20)

    ax.set_xticks(np.arange(len(index_names)))
    ax.set_yticks(np.arange(len(index_names)))
    ax.set_xticklabels(index_names)
    ax.set_yticklabels(index_names)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    for i in range(len(index_names)):
        for j in range(len(index_names)):
            ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.3f}', ha="center", va="center", color="black", fontsize=10)

    title = f'Correlation Matrix ({interval.capitalize()} Returns)'
    if start_date or end_date:
        date_range = []
        if start_date:
            date_range.append(f'from {start_date}')
        if end_date:
            date_range.append(f'to {end_date}')
        title += f'\n{" ".join(date_range)}'

    ax.set_title(title, fontsize=14, pad=20)
    plt.tight_layout()
    plt.show()
