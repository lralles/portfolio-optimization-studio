import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_drawdown(df, title, start_date=None, end_date=None):
    filtered_df = df.copy()
    
    if start_date is not None:
        filtered_df = filtered_df[filtered_df['date'] >= pd.to_datetime(start_date)]
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['date'] <= pd.to_datetime(end_date)]
    
    filtered_df = filtered_df.reset_index(drop=True)
    
    cumulative_max = filtered_df['price'].cummax()
    drawdown = ((filtered_df['price'] - cumulative_max) / cumulative_max) * 100
    
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(filtered_df['date'], drawdown, linewidth=1)
    ax.fill_between(filtered_df['date'], drawdown, 0, alpha=0.3)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Drawdown (%)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
