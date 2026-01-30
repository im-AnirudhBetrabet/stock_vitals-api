from fastapi import APIRouter, Query, Depends
from app.services.vitals_service import VitalsService

router = APIRouter()

@router.get("/stocks")
async def search_stocks(query: str = Query(..., min_length=2), service: VitalsService = Depends()):
    return await service.search_tickers(query)
