from app.db.vitals_repo import VitalsRepository
from app.models.analysis import AnalysisLogRead

class VitalsService:
    def __init__(self):
        self._repo = VitalsRepository()

    async def get_paginated_vitals(self, page: int, size: int):
        skip = (page - 1) * size
        data, total_count = await self._repo.fetch_paginated_logs(skip, size)


        items = [ AnalysisLogRead.model_validate(item) for item in data]

        return {
            "items" : items,
            "total" : total_count,
            "page"  : page,
            "size"  : size,
            "pages" : ( total_count + size - 1) // size if total_count else 0
        }
