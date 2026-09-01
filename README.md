# Portfolio Optimization Studio

Portfolio Optimization Studio is a Python project for analyzing historical financial index data, generating cleaned datasets, and exploring several investment-focused visualizations and portfolio analyses through Jupyter notebooks.

## What’s Inside

- `data/` is the expected location for raw input files supplied by the user.
- `sanitized_data/` stores cleaned CSV outputs created by ingestion.
- `src/ingestion/` contains functions that read, sanitize, sort, and export each dataset.
- `src/analysis/` contains the analysis and plotting logic used by the notebooks.
- `notebooks/` contains the Jupyter notebooks for ingestion and analysis.
- `docs/` contains project documentation and usage notes.

## Main Features

- Clean raw market data into a standard `date` / `price` format.
- Generate absolute price charts.
- Generate rentability charts based on percentage return from the initial price.
- Run comparative and portfolio-oriented analysis notebooks.

## Supported Data

The project includes analysis for several financial indexes and market series, including:

- IBOVESPA
- IFIX
- Bovespa Dividend Index
- S&P 500
- USD/BRL
- ANBIMA fixed income indexes such as IMA-B, IMA-B 5, IMA-S, IRF-M, and related series

## Data Availability

Market data is not included in this repository. Anyone wishing to use the
project should obtain the required historical data from an appropriate
external source and place the input files in `data/` before running the
ingestion notebook.

Documentation explaining how to obtain market data is currently being
prepared and will be added to this project as it becomes available.

## Requirements

- Python 3.12+
- A virtual environment at `.venv/`
- Dependencies listed in `requirements.txt`

## Setup

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Git Hook Setup

To keep notebook commits clean, enable the repository hook path once per clone:

```bash
git config --local core.hooksPath .githooks
```

The hook clears notebook output before commits and restages the notebooks automatically.

## How to Use

### 1. Run Data Ingestion

Open and run:

```bash
jupyter notebook notebooks/ingestion.ipynb
```

This notebook processes the raw files you provide in `data/` and generates sanitized CSV files in `sanitized_data/`.

### 2. Explore the Results

After ingestion, open the analysis notebooks you want to inspect:

```bash
jupyter notebook notebooks/absolute_price.ipynb
jupyter notebook notebooks/rentability.ipynb
```

Additional analysis notebooks are available in `notebooks/` for tasks such as correlation analysis, drawdown, efficient frontier exploration, portfolio optimization, rolling comparison, and risk-return analysis.

## Project Workflow

```text
Raw data in data/
  -> ingestion functions in src/ingestion/
  -> clean CSV files in sanitized_data/
  -> analysis logic in src/analysis/
  -> visual exploration in notebooks/
```

## Documentation

- [Getting Started](docs/GETTING_STARTED.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Project Structure](docs/STRUCTURE.md)

## Notes

- Market data must be obtained from external sources; it is not distributed with this project.
- The ingestion pipeline expects the raw source files you provide to be present in `data/`.
- The cleaned CSV files in `sanitized_data/` are generated artifacts.
- Notebook cells are designed to run from the project root after the path setup in the first cell.
