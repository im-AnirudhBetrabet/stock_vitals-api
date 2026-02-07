from app.db.vitals_repo import VitalsRepository
from app.models.analysis import StockCard, StockDetail
from app.utils.get_price_data import get_price_data

class VitalsService:
    def __init__(self):
        self._repo = VitalsRepository()


    async def get_paginated_vitals(self, page: int, size: int, track: str = None):
        skip = (page - 1) * size
        data, total_count = await self._repo.fetch_paginated_logs(skip, size, track)

        formatted_items = []
        tickers = [item["ticker"] for item in data]

        price_map = await get_price_data(tickers)

        for item in data:
            stock_info = item.get("stocks", {}) or {}
            ticker     = item["ticker"]
            prices     = price_map.get(ticker, {
                "current_price": 0.0, "day_high": 0.0, "day_low": 0.0, "previous_close": 0.0
            })
            price_change = 0.0 if prices["previous_close"] == 0.0 else round(((prices["current_price"] - prices["previous_close"]) / prices["previous_close"]) * 100, 3)
            formatted_items.append({
                "ticker"       : ticker,
                "company_name" : stock_info.get("name", "Unknown"),
                "final_score"  : item["final_score"],
                "timestamp"    : item["timestamp"],
                "current_price": prices["current_price"],
                "price_change" : price_change
            })

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
        ticker_list = list()
        ticker_list.append(ticker)

        price_data   = await get_price_data(ticker_list)
        price_data   = price_data.get(ticker)
        price_change = 0.0 if price_data.get("previous_close") == 0.0 else round(((price_data.get('current_price', 0.0) - price_data.get('previous_close', 0.0)) / price_data.get('previous_close', 0.0)) * 100, 2)
        price_data['price_change'] = price_change
        data['price_data']         = price_data

        return StockDetail.model_validate(data)

    async def search_tickers(self, query: str):
        if not query or len(query) < 2:
            return []
        return await self._repo.search_stocks(query)