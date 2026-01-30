from app.db.vitals_repo import VitalsRepository
from app.models.analysis import StockCard, StockDetail


class VitalsService:
    def __init__(self):
        self._repo = VitalsRepository()

    async def get_paginated_vitals(self, page: int, size: int, track: str = None):
        skip = (page - 1) * size
        data, total_count = await self._repo.fetch_paginated_logs(skip, size, track)

        formatted_items = []

        for item in data:
            stock_info = item.get("stocks", {}) or {}
            formatted_items.append({
                "ticker"      : item["ticker"],
                "company_name": stock_info.get("company_name", "Unknown"),
                "final_score" : item["final_score"],
                "timestamp"   : item["timestamp"]
            })

        # items = [ AnalysisLogRead.model_validate(item) for item in data]

        return {
            "items" : [StockCard(**item) for item in formatted_items],
            "total" : total_count,
            "page"  : page,
            "size"  : size,
            "pages" : ( total_count + size - 1) // size if total_count else 0
        }

    async def get_stock_metrics(self, ticker) -> StockDetail:
        """
        Business logic to retrieve and validate the StockDetails model
        :param ticker: Ticker for which the metrics is required.
        :return:
        """
        data = await self._repo.fetch_stock_details(ticker)

        if not data:
            return None

        return StockDetail.model_validate(data)