from typing import List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from .common_calculations.variations import get_day_variation, get_month_variation, get_year_variation

def plot_correlation_matrix(
    index_data_list: List[pd.DataFrame],
    index_names: List[str],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    interval: str = 'daily'
) -> None:
    if interval not in ['daily', 'month', 'year']:
        raise ValueError("interval must be 'daily', 'month', or 'year'")
    
    if len(index_data_list) != len(index_names):
        raise ValueError("index_data_list and index_names must have the same length")
    
    if interval == 'daily':
        variation_func = get_day_variation
    elif interval == 'month':
        variation_func = get_month_variation
    else:
        variation_func = get_year_variation
    
    variations_dict = {}
    for idx, (df, name) in enumerate(zip(index_data_list, index_names)):
        var_df = variation_func(df, start_date, end_date)
        variations_dict[name] = var_df.set_index('date')['variation']
    
    combined_df = pd.DataFrame(variations_dict)
    
    combined_df = combined_df.dropna()
    
    correlation_matrix = combined_df.corr()
    
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
            text = ax.text(j, i, f'{correlation_matrix.iloc[i, j]:.3f}',
                          ha="center", va="center", color="black", fontsize=10)
    
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
