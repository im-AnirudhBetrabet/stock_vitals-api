from fastapi import FastAPI
from app.api.v1.endpoints.vitals import router as vitals_router

app = FastAPI(title="Stock Vitals API", version= "1.0.0")

app.include_router(vitals_router, prefix="/api/v1/vitals", tags=["Vitals"])

@app.get("/")
async def root():
    return {
        "message" : "Stock Vitals API is live"
    }

