from fastapi import APIRouter, Query, Depends
from app.services.vitals_service import VitalsService

router =APIRouter()

@router.get("/all")
async def get_all_vitals(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), service: VitalsService = Depends()):
    """
    Returns a paginated list of stock vitals for the dashboard
    :param page:    Current page number
    :param size:    Number of results
    :param service:
    :return:
    """
    return await service.get_paginated_vitals(page, size)
