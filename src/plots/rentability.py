import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_rentability(df, title):
    initial_price = df['price'].iloc[0]
    rentability = ((df['price'] / initial_price) - 1) * 100
    
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df['date'], rentability, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Rentability (%)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
