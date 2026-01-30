
from fastapi import APIRouter, Query, Depends, HTTPException

from app.models.analysis import StockDetail
from app.services.vitals_service import VitalsService

router =APIRouter()

@router.get("/all", response_model=dict)
async def get_all_vitals(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), track:str = Query(None, description="Filter by: Makers, Scalers, or Lenders"), service: VitalsService = Depends()):
    """
    Returns a paginated list of stock vitals for the dashboard
    :param track:   Track to filter the data with.
    :param page:    Current page number
    :param size:    Number of results
    :param service:
    :return:
    """
    return await service.get_paginated_vitals(page, size, track)


@router.get("/details/{ticker}", response_model=StockDetail)
async def get_details(ticker: str, service: VitalsService = Depends()):
    """
    Endpoint to retrieve the metrics for the ticker.
    :param ticker: The ticker for which the metrics is required
    :param service:
    :return:
    """
    details = await service.get_stock_metrics(ticker)
    if not details:
        raise HTTPException(status_code=404, detail=f"Metrics for {ticker} not found")
    return details