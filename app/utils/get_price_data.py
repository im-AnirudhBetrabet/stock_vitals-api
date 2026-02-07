import yfinance as yf
import pandas as pd
import asyncio
from typing import Dict
from fastapi.concurrency import run_in_threadpool

async def get_price_data(tickers: list) -> Dict[str, dict]:
    def fetch():
        if not tickers:
            return {}
        ticker_str = " ".join(tickers) if len(tickers) > 1 else tickers
        try:
            data = yf.download(
                ticker_str,
                period="2d",
                group_by='ticker',
                threads=False,
                progress=False,
                auto_adjust=False
            )

            if data.empty:
                return {}

        except Exception as e:
            print(f"Yahoo Batch Download Failed: {e}")
            return {}

        prices = {}

        for ticker in tickers:
            try:
                df = data[ticker] if len(tickers) > 1 else data

                if df.empty or len(df) < 1:
                    continue

                latest_row = df.iloc[-1]

                if len(tickers) > 1:
                    prev_close = df['Close'].iloc[-2] if len(df) > 1 else 0.0
                    prices[ticker] = {
                        "current_price" : 0.0 if pd.isna(latest_row['Close']) else round(float(latest_row['Close']), 2),
                        "day_high"      : 0.0 if pd.isna(latest_row['High'])  else round(float(latest_row['High']), 2),
                        "day_low"       : 0.0 if pd.isna(latest_row['Low'])   else round(float(latest_row['Low']), 2),
                        "previous_close": 0.0 if pd.isna(prev_close) else round(float(prev_close), 2)
                    }
                else:
                    prev_close = df[ticker]['Close'].iloc[-2] if len(df) > 1 else 0.0
                    prices[ticker] = {
                        "current_price" : 0.0 if pd.isna(latest_row[ticker]['Close']) else round(float(latest_row[ticker]['Close']), 2),
                        "day_high"      : 0.0 if pd.isna(latest_row[ticker]['High'])  else round(float(latest_row[ticker]['High']), 2),
                        "day_low"       : 0.0 if pd.isna(latest_row[ticker]['Low'])   else round(float(latest_row[ticker]['Low']), 2),
                        "previous_close": 0.0 if pd.isna(prev_close) else round(float(prev_close), 2)
                    }

            except Exception as e:
                prices[ticker] = {
                    "current_price": 0.0, "day_high": 0.0, "day_low": 0.0, "previous_close": 0.0
                }
        return prices

    try:
        return await asyncio.wait_for(run_in_threadpool(fetch), timeout=15.0)
    except asyncio.TimeoutError:
        return {}