# Portfolio Optimization Studio

Portfolio Optimization Studio is a Python project for analyzing historical financial index data, generating cleaned datasets, and exploring several investment-focused visualizations and portfolio analyses through Jupyter notebooks.

## What’s Inside

- `data/` is the expected location for raw input files supplied by the user.
- `sanitized_data/` stores cleaned CSV outputs created by ingestion.
- `src/ingestion/` contains functions that read, sanitize, sort, and export each dataset.
- `src/analysis/` contains the analysis and plotting logic used by the notebooks.
- `src/application/` orchestrates consumer-backed analysis use cases for clients.
- `src/webapi/` exposes those use cases as a JSON HTTP API.
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

### 3. Start the API

From the project root, after installing the requirements:

```bash
uvicorn src.webapi.main:app --reload
```

The API is documented at `http://127.0.0.1:8000/docs`. Use `GET /api/v1/indexes` to list available consumer indexes. The first API version accepts index names and analysis parameters; custom weighted portfolios are intentionally not part of this surface yet.

To use the sample requests, open the `.bruno/` directory as a collection in Bruno, select the `local` environment, and run the requests against the running API. The collection includes one request for every endpoint.

### 4. Start the React frontend

In another terminal, with the API still running:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, usually `http://127.0.0.1:5173`. The frontend uses `http://127.0.0.1:8000` by default; set `VITE_API_BASE_URL` in `frontend/.env` if the API runs elsewhere.

## Project Workflow

```text
Raw data in data/
  -> ingestion functions in src/ingestion/
  -> clean CSV files in sanitized_data/
  -> analysis logic in src/analysis/
  -> application use cases in src/application/
  -> notebooks/ or web clients through src/webapi/
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
