from __future__ import annotations

from typing import Literal, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from src.application import AnalysisApplication
from src.webapi.serialization import to_jsonable


app = FastAPI(
    title="Portfolio Optimization Studio API",
    description="Consumer-backed historical index and portfolio analysis API.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
application = AnalysisApplication()


class IndexesRequest(BaseModel):
    indexes: list[str] = Field(min_length=1)
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CorrelationRequest(IndexesRequest):
    interval: Literal["daily", "month", "year"] = "daily"


class DiscountedRequest(BaseModel):
    measured_index: str
    reference_index: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class RollingComparisonRequest(BaseModel):
    index_a: str
    index_b: str
    window_years: float = Field(default=3.0, gt=0)
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class SlidingWindowRequest(IndexesRequest):
    window_size: int = Field(default=252, gt=0)


class RiskReturnSlidingWindowRequest(IndexesRequest):
    window_years: float = Field(default=3.0, gt=0)
    window_count: Optional[int] = Field(default=None, gt=0)
    independent_windows: bool = False


class EfficientFrontierRequest(IndexesRequest):
    risk_free_rate: float = 0.0
    n_points: int = Field(default=200, gt=0)


class PortfolioOptimizationRequest(IndexesRequest):
    window_size: int = Field(gt=0)
    sample_number: int = Field(gt=0)
    independent_windows: bool = False
    n_points: int = Field(default=200, gt=0)
    step_size: int = Field(default=10, gt=0, le=100)
    top_n: int = Field(default=10, gt=0)


class InflationBondsRequest(BaseModel):
    random_portfolios: int = Field(default=40, ge=0)
    seed: int = 42


def _response(value):
    return to_jsonable(value)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/indexes")
def indexes() -> dict[str, list[str]]:
    return {"indexes": application.available_indexes()}


@app.get("/api/v1/indexes/{index_name}/prices")
def prices(
    index_name: str,
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
):
    return _response(application.prices(index_name, start_date, end_date))


@app.get("/api/v1/indexes/{index_name}/rentability")
def rentability(
    index_name: str,
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
):
    return _response(application.rentability(index_name, start_date, end_date))


@app.get("/api/v1/indexes/{index_name}/drawdown")
def drawdown(
    index_name: str,
    start_date: Optional[str] = Query(default=None),
    end_date: Optional[str] = Query(default=None),
):
    return _response(application.drawdown(index_name, start_date, end_date))


@app.post("/api/v1/analyses/comparative")
def comparative(request: IndexesRequest):
    return _response(
        application.comparative(request.indexes, request.start_date, request.end_date)
    )


@app.post("/api/v1/analyses/correlation")
def correlation(request: CorrelationRequest):
    return _response(
        application.correlation(
            request.indexes,
            request.start_date,
            request.end_date,
            request.interval,
        )
    )


@app.post("/api/v1/analyses/discounted")
def discounted(request: DiscountedRequest):
    return _response(
        application.discounted(
            request.measured_index,
            request.reference_index,
            request.start_date,
            request.end_date,
        )
    )


@app.post("/api/v1/analyses/risk-return")
def risk_return(request: IndexesRequest):
    return _response(
        application.risk_return(request.indexes, request.start_date, request.end_date)
    )


@app.post("/api/v1/analyses/rolling-comparison")
def rolling_comparison(request: RollingComparisonRequest):
    return _response(
        application.rolling_comparison(
            request.index_a,
            request.index_b,
            request.window_years,
            request.start_date,
            request.end_date,
        )
    )


@app.post("/api/v1/analyses/sliding-window")
def sliding_window(request: SlidingWindowRequest):
    return _response(
        application.sliding_window(
            request.indexes,
            request.window_size,
            request.start_date,
            request.end_date,
        )
    )


@app.post("/api/v1/analyses/risk-return-sliding-window")
def risk_return_sliding_window(request: RiskReturnSlidingWindowRequest):
    return _response(
        application.risk_return_sliding_window(
            request.indexes,
            request.window_years,
            request.start_date,
            request.end_date,
            request.window_count,
            request.independent_windows,
        )
    )


@app.post("/api/v1/analyses/efficient-frontier")
def efficient_frontier(request: EfficientFrontierRequest):
    return _response(
        application.efficient_frontier(
            request.indexes,
            request.risk_free_rate,
            request.start_date,
            request.end_date,
            request.n_points,
        )
    )


@app.post("/api/v1/analyses/portfolio-optimization")
def portfolio_optimization(request: PortfolioOptimizationRequest):
    return _response(
        application.portfolio_optimization(
            request.indexes,
            request.window_size,
            request.sample_number,
            request.independent_windows,
            request.start_date,
            request.end_date,
            request.n_points,
            request.step_size,
            request.top_n,
        )
    )


@app.post("/api/v1/analyses/portfolio-return-optimization")
def portfolio_return_optimization(request: PortfolioOptimizationRequest):
    return _response(
        application.portfolio_return_optimization(
            request.indexes,
            request.window_size,
            request.sample_number,
            request.independent_windows,
            request.start_date,
            request.end_date,
            request.n_points,
            request.step_size,
            request.top_n,
        )
    )


@app.post("/api/v1/analyses/inflation-bonds-risk-return")
def inflation_bonds_risk_return(request: InflationBondsRequest):
    return _response(
        application.inflation_bonds_risk_return(
            request.random_portfolios,
            request.seed,
        )
    )


@app.exception_handler(ValueError)
async def value_error_handler(_, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(FileNotFoundError)
async def file_not_found_handler(_, exc: FileNotFoundError):
    return JSONResponse(
        status_code=503,
        content={"detail": f"Sanitized data is unavailable: {exc}"},
    )
