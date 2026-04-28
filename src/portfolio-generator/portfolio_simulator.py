import pandas as pd
from typing import List, Tuple
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from consumers import IndexData


def simulate_portfolio(
    portfolio: List[Tuple[IndexData, float]],
    start_date: str = None,
    end_date: str = None
) -> IndexData:
    if not portfolio:
        raise ValueError("Portfolio cannot be empty")
    
    total_weight = sum(weight for _, weight in portfolio)
    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1.0, got {total_weight}")
    
    dfs = []
    for index_data, weight in portfolio:
        df = index_data['data'].copy()
        df['weight'] = weight
        df['index_name'] = index_data['name']
        dfs.append(df)
    
    all_dates = set(dfs[0]['date'])
    for df in dfs[1:]:
        all_dates = all_dates.intersection(set(df['date']))
    
    if not all_dates:
        raise ValueError("No common dates found across all indices")
    
    all_dates = sorted(all_dates)
    
    if start_date:
        start_dt = pd.to_datetime(start_date)
        all_dates = [d for d in all_dates if d >= start_dt]
    
    if end_date:
        end_dt = pd.to_datetime(end_date)
        all_dates = [d for d in all_dates if d <= end_dt]
    
    if not all_dates:
        raise ValueError("No dates remaining after applying start/end date filters")
    
    filtered_dfs = []
    for df in dfs:
        filtered = df[df['date'].isin(all_dates)].sort_values('date').reset_index(drop=True)
        filtered_dfs.append(filtered)
    
    first_date = all_dates[0]
    initial_prices = {}
    for df in filtered_dfs:
        first_row = df[df['date'] == first_date].iloc[0]
        index_name = first_row['index_name']
        weight = first_row['weight']
        initial_price = first_row['price']
        initial_prices[index_name] = (initial_price, weight)
    
    portfolio_values = []
    for date in all_dates:
        portfolio_value = 0.0
        for df in filtered_dfs:
            row = df[df['date'] == date].iloc[0]
            index_name = row['index_name']
            current_price = row['price']
            initial_price, weight = initial_prices[index_name]
            
            shares = weight / initial_price
            portfolio_value += shares * current_price
        
        portfolio_values.append({'date': date, 'price': portfolio_value})
    
    result_df = pd.DataFrame(portfolio_values)
    
    return IndexData(name='portfolio', data=result_df)


def simulate_portfolio_rebalanced(
    portfolio: List[Tuple[IndexData, float]],
    start_date: str = None,
    end_date: str = None
) -> IndexData:
    if not portfolio:
        raise ValueError("Portfolio cannot be empty")
    
    total_weight = sum(weight for _, weight in portfolio)
    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1.0, got {total_weight}")
    
    dfs = []
    for index_data, weight in portfolio:
        df = index_data['data'].copy()
        df['weight'] = weight
        df['index_name'] = index_data['name']
        dfs.append(df)
    
    all_dates = set(dfs[0]['date'])
    for df in dfs[1:]:
        all_dates = all_dates.intersection(set(df['date']))
    
    if not all_dates:
        raise ValueError("No common dates found across all indices")
    
    all_dates = sorted(all_dates)
    
    if start_date:
        start_dt = pd.to_datetime(start_date)
        all_dates = [d for d in all_dates if d >= start_dt]
    
    if end_date:
        end_dt = pd.to_datetime(end_date)
        all_dates = [d for d in all_dates if d <= end_dt]
    
    if not all_dates:
        raise ValueError("No dates remaining after applying start/end date filters")
    
    filtered_dfs = []
    for df in dfs:
        filtered = df[df['date'].isin(all_dates)].sort_values('date').reset_index(drop=True)
        filtered_dfs.append(filtered)
    
    portfolio_value = 1.0
    portfolio_values = []
    
    for date in all_dates:
        daily_return = 0.0
        
        for df in filtered_dfs:
            row = df[df['date'] == date].iloc[0]
            weight = row['weight']
            
            if date == all_dates[0]:
                continue
            
            prev_date = all_dates[all_dates.index(date) - 1]
            prev_row = df[df['date'] == prev_date].iloc[0]
            
            asset_return = (row['price'] / prev_row['price']) - 1
            daily_return += weight * asset_return
        
        if date != all_dates[0]:
            portfolio_value *= (1 + daily_return)
        
        portfolio_values.append({'date': date, 'price': portfolio_value})
    
    result_df = pd.DataFrame(portfolio_values)
    
    return IndexData(name='portfolio_rebalanced', data=result_df)


def simulate_portfolio_rebalanced_monthly(
    portfolio: List[Tuple[IndexData, float]],
    start_date: str = None,
    end_date: str = None
) -> IndexData:
    if not portfolio:
        raise ValueError("Portfolio cannot be empty")
    
    total_weight = sum(weight for _, weight in portfolio)
    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1.0, got {total_weight}")
    
    dfs = []
    target_weights = {}
    for index_data, weight in portfolio:
        df = index_data['data'].copy()
        df['index_name'] = index_data['name']
        dfs.append(df)
        target_weights[index_data['name']] = weight
    
    all_dates = set(dfs[0]['date'])
    for df in dfs[1:]:
        all_dates = all_dates.intersection(set(df['date']))
    
    if not all_dates:
        raise ValueError("No common dates found across all indices")
    
    all_dates = sorted(all_dates)
    
    if start_date:
        start_dt = pd.to_datetime(start_date)
        all_dates = [d for d in all_dates if d >= start_dt]
    
    if end_date:
        end_dt = pd.to_datetime(end_date)
        all_dates = [d for d in all_dates if d <= end_dt]
    
    if not all_dates:
        raise ValueError("No dates remaining after applying start/end date filters")
    
    filtered_dfs = []
    for df in dfs:
        filtered = df[df['date'].isin(all_dates)].sort_values('date').reset_index(drop=True)
        filtered_dfs.append(filtered)
    
    portfolio_value = 1.0
    portfolio_values = []
    last_rebalance_month = None
    shares = {}
    
    for i, date in enumerate(all_dates):
        current_month = (date.year, date.month)
        should_rebalance = (last_rebalance_month is None or current_month != last_rebalance_month)
        
        if i > 0:
            portfolio_value = 0.0
            for df in filtered_dfs:
                row = df[df['date'] == date].iloc[0]
                index_name = row['index_name']
                current_price = row['price']
                portfolio_value += shares[index_name] * current_price
        
        if should_rebalance:
            for df in filtered_dfs:
                row = df[df['date'] == date].iloc[0]
                index_name = row['index_name']
                current_price = row['price']
                target_weight = target_weights[index_name]
                shares[index_name] = (portfolio_value * target_weight) / current_price
            
            last_rebalance_month = current_month
        
        portfolio_values.append({'date': date, 'price': portfolio_value})
    
    result_df = pd.DataFrame(portfolio_values)
    
    return IndexData(name='portfolio_rebalanced_monthly', data=result_df)


def simulate_portfolio_rebalanced_yearly(
    portfolio: List[Tuple[IndexData, float]],
    start_date: str = None,
    end_date: str = None
) -> IndexData:
    if not portfolio:
        raise ValueError("Portfolio cannot be empty")
    
    total_weight = sum(weight for _, weight in portfolio)
    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1.0, got {total_weight}")
    
    dfs = []
    target_weights = {}
    for index_data, weight in portfolio:
        df = index_data['data'].copy()
        df['index_name'] = index_data['name']
        dfs.append(df)
        target_weights[index_data['name']] = weight
    
    all_dates = set(dfs[0]['date'])
    for df in dfs[1:]:
        all_dates = all_dates.intersection(set(df['date']))
    
    if not all_dates:
        raise ValueError("No common dates found across all indices")
    
    all_dates = sorted(all_dates)
    
    if start_date:
        start_dt = pd.to_datetime(start_date)
        all_dates = [d for d in all_dates if d >= start_dt]
    
    if end_date:
        end_dt = pd.to_datetime(end_date)
        all_dates = [d for d in all_dates if d <= end_dt]
    
    if not all_dates:
        raise ValueError("No dates remaining after applying start/end date filters")
    
    filtered_dfs = []
    for df in dfs:
        filtered = df[df['date'].isin(all_dates)].sort_values('date').reset_index(drop=True)
        filtered_dfs.append(filtered)
    
    portfolio_value = 1.0
    portfolio_values = []
    last_rebalance_year = None
    shares = {}
    
    for i, date in enumerate(all_dates):
        current_year = date.year
        should_rebalance = (last_rebalance_year is None or current_year != last_rebalance_year)
        
        if i > 0:
            portfolio_value = 0.0
            for df in filtered_dfs:
                row = df[df['date'] == date].iloc[0]
                index_name = row['index_name']
                current_price = row['price']
                portfolio_value += shares[index_name] * current_price
        
        if should_rebalance:
            for df in filtered_dfs:
                row = df[df['date'] == date].iloc[0]
                index_name = row['index_name']
                current_price = row['price']
                target_weight = target_weights[index_name]
                shares[index_name] = (portfolio_value * target_weight) / current_price
            
            last_rebalance_year = current_year
        
        portfolio_values.append({'date': date, 'price': portfolio_value})
    
    result_df = pd.DataFrame(portfolio_values)
    
    return IndexData(name='portfolio_rebalanced_yearly', data=result_df)
