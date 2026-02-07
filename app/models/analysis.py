from pydantic import BaseModel, ConfigDict
from typing import Dict, Any, Optional
from datetime import datetime

class StockCard(BaseModel):
    ticker       : str
    company_name : Optional[str] = None
    final_score  : float
    current_price: float = 0.0
    price_change : Optional[float] = 0.0
    timestamp    : datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class StockDetail(StockCard):
    track_used       : str
    accelerator_score: float
    quality_score    : float
    bargain_score    : float
    raw_metrics      : Dict[str, Any]
    metric_scores    : Dict[str, Any]
