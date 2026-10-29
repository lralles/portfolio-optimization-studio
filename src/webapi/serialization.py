from __future__ import annotations

from dataclasses import fields, is_dataclass
from datetime import date, datetime
from typing import Any

import numpy as np
import pandas as pd


def _scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (pd.Timestamp, datetime, date)):
        return value.isoformat()
    if value is pd.NaT:
        return None
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def to_jsonable(value: Any) -> Any:
    """Convert analysis results into values accepted by a JSON response."""
    if isinstance(value, pd.DataFrame):
        frame = value if isinstance(value.index, pd.RangeIndex) else value.reset_index()
        return [
            {str(key): to_jsonable(item) for key, item in row.items()}
            for row in frame.to_dict(orient="records")
        ]
    if isinstance(value, pd.Series):
        series_name = value.name or "value"
        return to_jsonable(value.rename(series_name).to_frame().reset_index())
    if is_dataclass(value):
        return {
            field.name: to_jsonable(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return [to_jsonable(item) for item in value.tolist()]
    return _scalar(value)
