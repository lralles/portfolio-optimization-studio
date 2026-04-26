import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_and_plot_rentability(df, title):
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
    
    total_return = rentability.iloc[-1]
    years = (df['date'].iloc[-1] - df['date'].iloc[0]).days / 365.25
    annualized_return = ((1 + total_return / 100) ** (1 / years) - 1) * 100
    
    return pd.DataFrame({
        'total_return': [total_return],
        'annualized_return': [annualized_return]
    })
