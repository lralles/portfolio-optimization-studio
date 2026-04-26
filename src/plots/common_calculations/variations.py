import pandas as pd
from typing import Optional

def get_day_variation(df: pd.DataFrame, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    filtered_df = df.copy()
    
    if start_date is not None:
        filtered_df = filtered_df[filtered_df['date'] >= pd.to_datetime(start_date)]
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['date'] <= pd.to_datetime(end_date)]
    
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df = filtered_df.sort_values('date')
    
    filtered_df['variation'] = filtered_df['price'].pct_change() * 100
    
    return filtered_df[['date', 'variation']].dropna()

def get_month_variation(df: pd.DataFrame, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    filtered_df = df.copy()
    
    if start_date is not None:
        filtered_df = filtered_df[filtered_df['date'] >= pd.to_datetime(start_date)]
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['date'] <= pd.to_datetime(end_date)]
    
    filtered_df = filtered_df.sort_values('date')
    filtered_df['year_month'] = filtered_df['date'].dt.to_period('M')
    
    monthly_df = filtered_df.groupby('year_month').agg({
        'date': 'last',
        'price': 'last'
    }).reset_index(drop=True)
    
    monthly_df['variation'] = monthly_df['price'].pct_change() * 100
    
    return monthly_df[['date', 'variation']].dropna()

def get_year_variation(df: pd.DataFrame, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    filtered_df = df.copy()
    
    if start_date is not None:
        filtered_df = filtered_df[filtered_df['date'] >= pd.to_datetime(start_date)]
    if end_date is not None:
        filtered_df = filtered_df[filtered_df['date'] <= pd.to_datetime(end_date)]
    
    filtered_df = filtered_df.sort_values('date')
    filtered_df['year'] = filtered_df['date'].dt.year
    
    yearly_df = filtered_df.groupby('year').agg({
        'date': 'last',
        'price': 'last'
    }).reset_index(drop=True)
    
    yearly_df['variation'] = yearly_df['price'].pct_change() * 100
    
    return yearly_df[['date', 'variation']].dropna()
