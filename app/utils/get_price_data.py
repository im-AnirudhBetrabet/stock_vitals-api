import yfinance as yf
import pandas as pd
import asyncio
from typing import Dict
from fastapi.concurrency import run_in_threadpool


async def get_price_data(tickers: list) -> Dict[str, float]:
    """Helper to fetch a single stock price safely"""
    """
            Fetches ALL prices in a SINGLE request.
            Solves the timeout issue by avoiding 10 separate connections.
            """

    def fetch():
        if not tickers:
            return {}

        tickers_str = " ".join(tickers)

        try:
            # threads=False is safer here as we are already in a threadpool
            data = yf.download(
                tickers_str,
                period="1d",
                group_by='ticker',
                threads=False,
                progress=False
            )
        except Exception as e:
            print(f"Yahoo Batch Download Failed: {e}")
            return {}

        prices = {}
        for ticker in tickers:
            try:
                # Initialize default values
                price_data = {
                    "current_price": 0.0,
                    "day_high": 0.0,
                    "day_low": 0.0,
                    "previous_close": 0.0
                }

                if len(tickers) > 1:
                    if ticker in data.columns.levels[0]:
                        ticker_data = data[ticker]
                        price_data["current_price"] = 0.0 if pd.isna(ticker_data['Close'].iloc[-1]) else round(
                            float(ticker_data['Close'].iloc[-1]), 2)
                        price_data["day_high"] = 0.0 if pd.isna(ticker_data['High'].iloc[-1]) else round(
                            float(ticker_data['High'].iloc[-1]), 2)
                        price_data["day_low"] = 0.0 if pd.isna(ticker_data['Low'].iloc[-1]) else round(
                            float(ticker_data['Low'].iloc[-1]), 2)
                        price_data["previous_close"] = 0.0 if pd.isna(ticker_data['Open'].iloc[-1]) else round(
                            float(ticker_data['Open'].iloc[-1]), 2)
                else:
                    # Single ticker dataframe structure is different (flat)
                    price_data["current_price"] = 0.0 if pd.isna(data['Close'].iloc[-1]) else round(
                        float(data['Close'].iloc[-1]), 2)
                    price_data["day_high"] = 0.0 if pd.isna(data['High'].iloc[-1]) else round(
                        float(data['High'].iloc[-1]), 2)
                    price_data["day_low"] = 0.0 if pd.isna(data['Low'].iloc[-1]) else round(float(data['Low'].iloc[-1]),
                                                                                            2)
                    price_data["previous_close"] = 0.0 if pd.isna(data['Open'].iloc[-1]) else round(
                        float(data['Open'].iloc[-1]), 2)

                prices[ticker] = price_data

            except Exception as e:
                # If one fails, just return defaults for that one
                prices[ticker] = {
                    "current_price": 0.0, "day_high": 0.0, "day_low": 0.0, "previous_close": 0.0
                }

        return prices

    # Run in threadpool with a safety timeout
    try:
        return await asyncio.wait_for(run_in_threadpool(fetch), timeout=10.0)
    except asyncio.TimeoutError:
        print("Batch price fetch timed out")
        return {}