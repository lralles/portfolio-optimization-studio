import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_absolute_price(df, title):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(df['date'], df['price'], linewidth=1)
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
