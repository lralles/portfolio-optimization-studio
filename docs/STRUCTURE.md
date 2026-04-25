# Project Structure

## Directory Layout

```
investing-analyser/
├── docs/                          # Documentation
│   ├── PROJECT_OVERVIEW.md       # What this project does
│   ├── STRUCTURE.md              # This file - folder organization
│   └── GETTING_STARTED.md        # How to run the analysis
│
├── notebooks/                     # Jupyter notebooks
│   ├── main.ipynb                # Project overview & links
│   ├── ingestion.ipynb           # Run data ingestion pipeline
│   ├── absolute_price.ipynb      # Plot absolute prices
│   └── rentability.ipynb         # Plot rentability (%)
│
├── src/                           # Source code
│   ├── ingestion/                # Data ingestion modules
│   │   ├── ingest_bovespa.py
│   │   ├── ingest_ifix.py
│   │   ├── ingest_bovespa_dividend.py
│   │   ├── ingest_sp500.py
│   │   ├── ingest_usdbrl.py
│   │   ├── ingest_imab5.py
│   │   ├── ingest_imab5mais.py
│   │   ├── ingest_imab.py
│   │   ├── ingest_imas.py
│   │   ├── ingest_irfm1.py
│   │   ├── ingest_irfm1mais.py
│   │   └── ingest_irfm.py
│   │
│   └── plots/                    # Visualization modules
│       ├── absolute_price.py     # plot_absolute_price()
│       └── rentability.py        # plot_rentability()
│
├── data/                          # Raw data files (input)
│   ├── Bovespa Historical Data day.csv
│   ├── Bovespa Historical Data day 2.csv
│   ├── Bovespa Historical Data day 3.csv
│   ├── BM&FBOVESPA Real Estate IFIX Historical Data day.csv
│   ├── Bovespa Dividend Historical Data day.csv
│   ├── S&P 500 Historical Data day.csv
│   ├── USD_BRL Historical Data day.csv
│   ├── IMAB5-HISTORICO.xls
│   ├── IMAB5MAIS-HISTORICO.xls
│   ├── IMAB-HISTORICO.xls
│   ├── IMAS-HISTORICO.xls
│   ├── IRFM1-HISTORICO.xls
│   ├── IRFM1MAIS-HISTORICO.xls
│   └── IRFM-HISTORICO.xls
│
├── sanitized_data/                # Processed data (output)
│   ├── bovespa.csv
│   ├── ifix.csv
│   ├── bovespa_dividend.csv
│   ├── sp500.csv
│   ├── usdbrl.csv
│   ├── imab5.csv
│   ├── imab5mais.csv
│   ├── imab.csv
│   ├── imas.csv
│   ├── irfm1.csv
│   ├── irfm1mais.csv
│   └── irfm.csv
│
├── requirements.txt               # Python dependencies
├── AGENTS.md                      # Guidelines for code agents
└── .venv/                         # Python virtual environment
```

## Key Components

### src/ingestion/
Each file contains a function `ingest_<name>()` that:
- Reads raw data from `data/`
- Sanitizes and normalizes the data
- Outputs clean CSV with `date` and `price` columns
- Saves to `sanitized_data/<name>.csv`

**Supported Formats:**
- **CSV Files** - Direct parsing with pandas
- **XLS Files** - Read using openpyxl/xlrd engines

### src/plots/
Plotting utilities that take a DataFrame and create visualizations:

- **absolute_price.py** - `plot_absolute_price(df, title)`
  - Shows exact price values on Y-axis
  - Useful for comparing price ranges
  
- **rentability.py** - `plot_rentability(df, title)`
  - Shows percentage return from initial price: `((price / initial_price) - 1) * 100`
  - Useful for comparing relative performance
  - Example: price doubles → shows 100%

### notebooks/
Jupyter notebooks that orchestrate the analysis:

- **main.ipynb** - Overview and navigation
- **ingestion.ipynb** - Data processing (run first!)
- **absolute_price.ipynb** - View charts with absolute prices
- **rentability.ipynb** - View charts with percentage returns

All notebooks are self-contained and can be run independently.

## Data Flow

```
Raw Files (data/)
    └─ CSV files (Investing.com data)
    └─ XLS files (ANBIMA data)
       │
       ↓
Ingestion Functions (src/ingestion/)
       │
       └─ Normalize column names
       └─ Parse dates
       └─ Convert to numeric
       └─ Remove duplicates
       └─ Sort by date
       │
       ↓
Sanitized Files (sanitized_data/)
       │
       └─ One CSV per index
       └─ Columns: date, price
       │
       ↓
Notebooks (notebooks/)
       │
       └─ Read CSV
       └─ Create plots
       └─ Display in Jupyter
```

## File Naming Conventions

- **Ingestion files**: `ingest_<index_name>.py`
- **Sanitized data**: `<index_name>.csv`
- **Notebooks**: `<analysis_type>.ipynb`

## Dependencies

See `requirements.txt`:
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `matplotlib` - Visualization
- `openpyxl` / `xlrd` - Excel file reading

All managed in `.venv/` virtual environment.
