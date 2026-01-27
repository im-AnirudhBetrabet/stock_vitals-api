from app.db.supabase import supabase

class VitalsRepository:
    def __init__(self):
        self._client = supabase


    async def fetch_paginated_logs(self, skip: int, limit: int):
        """
        Fetches a slice of the analysis logs
        :param skip: The starting index
        :param limit: How many records to fetch
        :return:
        """

        stop = skip + limit - 1
        response = (self._client.table("analysis_logs")
                    .select("*", count="exact")
                    .order("timestamp", desc=True)
                    .range(skip, stop).execute()
                    )
        return response.data, response.count