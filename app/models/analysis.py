from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any
from datetime import datetime

class AnalysisLog(BaseModel):
    ticker    : str = Field(..., pattern=r'[A-Z0-9]+\.(NS|BO)$')
    track_used: str = Field(..., description="Makers, Lenders, or Scalers")

    final_score      : float = Field(..., ge=0, le=100)
    accelerator_score: float = Field(..., ge=0, le=100)
    quality_score    : float = Field(..., ge=0, le=100)
    bargain_score    : float = Field(..., ge=0, le=100)

    metric_scores: Dict[str, Any] = Field(..., description="Point breakdown for each metric")
    raw_metrics  : Dict[str, Any] = Field(..., description="Raw Financial data from yfinance")


class AnalysisLogRead(AnalysisLog):
    """
    Schema for the FastAPI app to use when returning data to the Frontend.
    """
    timestamp: datetime
    id       : int

    model_config = ConfigDict(from_attributes=True)