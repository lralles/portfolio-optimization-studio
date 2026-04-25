# Investing Analyser - Project Overview

## What is this project?

**Investing Analyser** is a data analysis tool that processes historical financial index data and provides visualizations in two formats:
1. **Absolute Price Charts** - Shows the exact price values over time
2. **Rentability Charts** - Shows percentage return (%) from the initial price point

## Supported Indexes

The project analyzes 12 different financial indexes:

### Brazilian Indexes
- **IBOVESPA (Bovespa)** - Brazilian stock exchange index
- **IFIX** - BM&FBOVESPA Real Estate Index
- **Bovespa Dividend Index** - Dividend performance

### International Indexes
- **S&P 500** - US stock market index
- **USD/BRL** - US Dollar to Brazilian Real exchange rate

### Bond Indexes (ANBIMA)
- **IMA-B 5** - ANBIMA Fixed Income Index (up to 5 years)
- **IMA-B 5+** - ANBIMA Fixed Income Index (over 5 years)
- **IMA-B** - ANBIMA Fixed Income Index (general)
- **IMA-S** - ANBIMA Sector Index
- **IRF-M 1** - ANBIMA Interest Rate Index (up to 1 year)
- **IRF-M 1+** - ANBIMA Interest Rate Index (over 1 year)
- **IRF-M** - ANBIMA Interest Rate Index (general)

## How It Works

### Data Processing Pipeline

1. **Data Ingestion** (`src/ingestion/`)
   - Each index has a dedicated ingestion function
   - Functions read raw data files (CSV or XLS format)
   - Data is sanitized and normalized
   - Output: Clean CSV files with only `date` and `price` columns

2. **Data Storage** (`sanitized_data/`)
   - Cleaned data stored in simple CSV format
   - Consistent structure across all indexes
   - Easy to parse and analyze

3. **Visualization** (`src/plots/`)
   - Two plot types available:
     - `absolute_price.py` - Shows exact price values
     - `rentability.py` - Shows percentage return from initial price
   - Both use matplotlib for rendering

### Workflow

```
Raw Data (data/) 
    ↓
Ingestion Functions (src/ingestion/)
    ↓
Sanitized Data (sanitized_data/)
    ↓
Plot Functions (src/plots/)
    ↓
Notebooks (notebooks/) - Visualization
```

## Notebooks

### 1. ingestion.ipynb
- Runs all 12 data ingestion functions
- Creates sanitized CSV files in `sanitized_data/`
- **Run this first** to process all raw data

### 2. absolute_price.ipynb
- Displays absolute price charts for all 12 indexes
- Y-axis shows exact price values
- Useful for comparing absolute price ranges

### 3. rentability.ipynb
- Displays rentability (%) charts for all 12 indexes
- Y-axis shows percentage return from initial price
- When price doubles from initial, shows 100%
- Useful for comparing relative performance

## Key Features

✓ **Modular Design** - Each index has its own ingestion module
✓ **Clean Data** - Automatic normalization and sanitization
✓ **Multiple Views** - Compare indexes using absolute or relative metrics
✓ **Low Overhead** - Simple CSV storage, no database required
✓ **Extensible** - Easy to add new indexes or visualization types
✓ **Warning Suppression** - Clean output without openpyxl warnings

## Data Sources

- **CSV Data** - Downloaded from Investing.com
- **XLS Data** - ANBIMA historical index files
- **Coverage** - Historical data from early 2000s to October 2024

## Next Steps

See `GETTING_STARTED.md` for instructions on how to run the analysis.
