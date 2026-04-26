import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_drawdown(df, title):
    cumulative_max = df['price'].cummax()
    drawdown = ((df['price'] - cumulative_max) / cumulative_max) * 100
    
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df['date'], drawdown, linewidth=1)
    ax.fill_between(df['date'], drawdown, 0, alpha=0.3)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Drawdown (%)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
