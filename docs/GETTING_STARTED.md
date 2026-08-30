# Getting Started

## Prerequisites

- Python 3.12+
- Virtual environment (.venv) already set up
- All dependencies installed from `requirements.txt`

## Git Hook Setup

To keep notebook commits clean, enable the repo hook path once per clone:

```bash
git config --local core.hooksPath .githooks
```

After that, the pre-commit hook will run `.venv/bin/jupyter nbconvert --to notebook --clear-output --inplace` on staged `.ipynb` files and restage them before each commit.

## Quick Start

### Step 1: Activate Virtual Environment

```bash
source .venv/bin/activate
```

### Step 2: Run Data Ingestion

Open and run `notebooks/ingestion.ipynb`:

```bash
jupyter notebook notebooks/ingestion.ipynb
```

This will:
- Import all 12 ingestion functions
- Process raw data from `data/` folder
- Generate sanitized CSV files in `sanitized_data/`
- Print "All ingestions complete!" when done

**⚠️ Important:** Run this notebook first before viewing charts!

### Step 3: View Analysis Results

After ingestion completes, you can open either visualization notebook:

#### Option A: View Absolute Prices
```bash
jupyter notebook notebooks/absolute_price.ipynb
```

Shows exact price values for all 12 indexes. Useful for:
- Comparing price ranges
- Understanding absolute values
- Tracking price magnitude over time

#### Option B: View Rentability (%)
```bash
jupyter notebook notebooks/rentability.ipynb
```

Shows percentage return from initial price. Useful for:
- Comparing relative performance
- Normalizing different indexes
- Understanding investment returns
- Example: If price doubles, shows 100%

## Workflow Example

1. **Process Data**
   ```bash
   # Run ingestion.ipynb
   # Waits for completion...
   # Files appear in sanitized_data/
   ```

2. **Compare Absolute Prices**
   ```bash
   # Run absolute_price.ipynb
   # See charts showing exact prices
   ```

3. **Compare Relative Performance**
   ```bash
   # Run rentability.ipynb
   # See charts showing percentage gains/losses
   ```

## How to Use Notebooks

Each notebook follows this pattern:

```python
# Cell 1: Imports
import sys
import pandas as pd
sys.path.insert(0, '..')
os.chdir('..')
from src.plots.absolute_price import plot_absolute_price

# Cell 2+: Load data and plot
df = pd.read_csv('sanitized_data/bovespa.csv', parse_dates=['date'])
plot_absolute_price(df, 'Bovespa (IBOVESPA)')
```

### Running Individual Cells

In Jupyter:
- Click on a cell
- Press `Shift + Enter` to execute
- Charts appear below the cell

### Running All Cells

- **Keyboard**: `Ctrl + A` → `Shift + Enter` (or use menu)
- **Menu**: Cell → Run All
- Generates all 12 charts in sequence

## Data Details

### Ingestion Process

Each ingestion function:
1. Reads raw file(s) from `data/`
2. Selects only `Date` and `Price` columns
3. Normalizes column names to lowercase (`date`, `price`)
4. Parses dates to datetime format
5. Converts prices to float
6. Removes duplicates
7. Sorts by date (ascending)
8. Saves to CSV

### Output Format

All sanitized CSV files have this structure:

```csv
date,price
2000-01-31,1394.5
2000-02-01,1420.25
...
```

- **date**: ISO format YYYY-MM-DD
- **price**: Decimal number (float)

## Rentability Calculation

Rentability is calculated as percentage return from the first price:

```
rentability(%) = ((price / first_price) - 1) × 100
```

Examples:
- If price stays same: 0%
- If price doubles: 100%
- If price is half: -50%
- If price is 1.5x: 50%

This allows comparing very different indexes on the same scale.

## Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

**Solution:** Make sure you're running notebooks from the `notebooks/` folder. Jupyter should auto-handle the path setup.

### "FileNotFoundError: sanitized_data/..."

**Solution:** Run `ingestion.ipynb` first to generate the CSV files.

### No plots showing

**Solution:** Make sure matplotlib is configured for notebook display:
- Add to first cell: `%matplotlib inline`
- Notebooks already have this, so should work automatically

### Openpyxl warnings

**Solution:** Already suppressed in ingestion functions. Should not see warnings.

## Project Map

For detailed information:
- **PROJECT_OVERVIEW.md** - What the project does
- **STRUCTURE.md** - Folder organization
- **GETTING_STARTED.md** - This file

## Next Steps

After running the analysis:
- Compare absolute prices vs. rentability views
- Identify best performing indexes
- Track performance over time
- Analyze correlations between indexes
- Export data for further analysis

Enjoy your analysis! 📊
