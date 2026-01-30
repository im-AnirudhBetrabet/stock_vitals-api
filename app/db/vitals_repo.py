from app.db.supabase import supabase

class VitalsRepository:
    def __init__(self):
        self._client = supabase


    async def fetch_paginated_logs(self, skip: int, limit: int, track: str = None):
        """
        Fetches a slice of the analysis logs
        :param track:
        :param skip: The starting index
        :param limit: How many records to fetch
        :return:
        """


        columns = "ticker, final_score, timestamp, stocks(name)"

        # Base query
        query = self._client.table("latest_stock_vitals").select(columns, count="exact")

        # Apply track filter is track is not 'All'
        if track is not None and track.lower() != 'all':
            query = query.eq("track_used", track.upper())

        stop = skip + limit - 1

        response = query.order("final_score", desc=True).range(skip, stop).execute()

        return response.data, response.count

    async def fetch_stock_details(self, ticker: str) -> dict | None:
        """
        Fetches the full breakdown and raw metrics for a ticker.
        :param ticker: Ticker for which the metrics are required
        :return: calculated metrics.
        """

        response = self._client.table("latest_stock_vitals").select("*").eq("ticker", ticker.upper()).single().execute()
        print(f"Response >>{response}")
        return response.data if response.data else None