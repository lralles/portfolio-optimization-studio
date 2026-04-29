from typing import Optional, Dict
import pandas as pd

def compute_discounted_analysis(measured: dict, reference: dict, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
    measured_df = measured['data'].sort_values('date').reset_index(drop=True)
    reference_df = reference['data'].sort_values('date').reset_index(drop=True)

    measured_name = measured['name']
    reference_name = reference['name']

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

    years = (aligned['date'].iloc[-1] - aligned['date'].iloc[0]).days / 365.25

    results = []
    for series_name, return_series in [
        (f'{measured_name} return', measured_return),
        (f'{reference_name} return', reference_return),
        (f'{measured_name} discounted by {reference_name}', discounted_return)
    ]:
        total_return = return_series.iloc[-1]
        annualized_return = ((1 + total_return / 100) ** (1 / years) - 1) * 100
        results.append({
            'series': series_name,
            'total_return': total_return,
            'annualized_return': annualized_return
        })

    return {
        'aligned': aligned,
        'measured_return': measured_return,
        'reference_return': reference_return,
        'discounted_return': discounted_return,
        'results_df': pd.DataFrame(results),
        'measured_name': measured_name,
        'reference_name': reference_name,
        'start_date': common_start,
        'end_date': common_end
    }
