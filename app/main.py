from fastapi import FastAPI
from app.api.v1.endpoints import vitals, search

app = FastAPI(title="Stock Vitals API", version= "1.0.0")

app.include_router(vitals.router, prefix="/api/v1/vitals", tags=["Vitals"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])

@app.get("/")
async def root():
    return {
        "message" : "Stock Vitals API is live"
    }

