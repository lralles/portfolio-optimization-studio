import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path


def plot_discounted_analysis(measured, reference, title, start_date=None, end_date=None):
    measured_df = pd.read_csv(Path('sanitized_data') / f'{measured}.csv', parse_dates=['date'])
    reference_df = pd.read_csv(Path('sanitized_data') / f'{reference}.csv', parse_dates=['date'])

    measured_df = measured_df.sort_values('date').reset_index(drop=True)
    reference_df = reference_df.sort_values('date').reset_index(drop=True)

    common_start = max(measured_df['date'].iloc[0], reference_df['date'].iloc[0])
    common_end = min(measured_df['date'].iloc[-1], reference_df['date'].iloc[-1])

    if start_date is not None:
        common_start = max(common_start, pd.to_datetime(start_date))
    if end_date is not None:
        common_end = min(common_end, pd.to_datetime(end_date))

    if common_start > common_end:
        raise ValueError('No overlapping date range found for the selected period.')

    measured_filtered = measured_df[(measured_df['date'] >= common_start) & (measured_df['date'] <= common_end)].reset_index(drop=True)
    reference_filtered = reference_df[(reference_df['date'] >= common_start) & (reference_df['date'] <= common_end)].reset_index(drop=True)

    aligned = pd.merge_asof(
        measured_filtered[['date', 'price']].sort_values('date'),
        reference_filtered[['date', 'price']].sort_values('date'),
        on='date',
        direction='backward',
        suffixes=('_measured', '_reference')
    ).dropna().reset_index(drop=True)

    if aligned.empty:
        raise ValueError('No aligned rows found after matching measured and reference dates.')

    measured_return = ((aligned['price_measured'] / aligned['price_measured'].iloc[0]) - 1) * 100
    reference_return = ((aligned['price_reference'] / aligned['price_reference'].iloc[0]) - 1) * 100
    discounted_return = (((aligned['price_measured'] / aligned['price_measured'].iloc[0]) / (aligned['price_reference'] / aligned['price_reference'].iloc[0])) - 1) * 100

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(aligned['date'], measured_return, linewidth=1, label=f'{measured} return')
    ax.plot(aligned['date'], reference_return, linewidth=1, label=f'{reference} return')
    ax.plot(aligned['date'], discounted_return, linewidth=1.5, label=f'{measured} discounted by {reference}')

    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Return (%)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    fig.autofmt_xdate()
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    plt.show()
