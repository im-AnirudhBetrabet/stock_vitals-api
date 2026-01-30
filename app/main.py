from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import vitals, search
from dotenv import load_dotenv
import os


load_dotenv()

app = FastAPI(title="Stock Vitals API", version= "1.0.0")

raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
origins = [origin.strip() for origin in raw_origins.split(",")]


app.add_middleware(
    CORSMiddleware, # type: ignore
    allow_origins=origins,            # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],              # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],              # Allows all headers
)


app.include_router(vitals.router, prefix="/api/v1/vitals", tags=["Vitals"])
app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])

@app.get("/")
async def root():
    return {
        "message" : "Stock Vitals API is live"
    }

