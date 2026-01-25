from http.client import responses

import pytest
from postgrest import APIError

from app.db.supabase import db_manager

TEST_TICKER = "TEST.NS"
DUMMY_STOCK = {
    "ticker"    : TEST_TICKER,
    "sector"    : "test_sector",
    "industry"  : "test_industry",
    "name"      : "test_stock_name",
    "last_price": 1.01
}

DUMMY_LOG = {
    "ticker": TEST_TICKER,
    "final_score": 75.0,
    "accelerator_score": 20.0,
    "quality_score": 15.0,
    "bargain_score": 40.0,
    "raw_metrics": {"pe": 20, "roe": 15},
    "metric_scores": {"acc": 20, "qual": 15, "barg": 40},
    "track_used": "Maker"
}

def test_anon_client_cannot_insert():
    """
    Scenario: Verify RLS blocks the public key from writing.
    Expected: Database should reject the request.
    """
    anon_client = db_manager.client
    with pytest.raises(APIError) as excinfo:
        anon_client.table("analysis_logs").insert(DUMMY_LOG).execute()

    # Assert that the error code is specifically for RLS/Permissions
    assert excinfo.value.code == "42501", "Public key should not be able to write due to RLS"

def test_service_client_can_insert_and_delete():
    """
    Scenario: Verify the service_role bypasses RLS.
    Expected: service_role should bypass the RLS.
    """
    service_client = db_manager.get_service_client()
    # 1. Insert data into
    insert_stock_res = service_client.table("stocks").insert(DUMMY_STOCK).execute()
    assert len(insert_stock_res.data) > 0, "Service role should bypass RLS and insert stock data"

    # 2. Insert into analysis logs (Bypass RLS)
    insert_logs_res = service_client.table("analysis_logs").insert(DUMMY_LOG).execute()
    assert len(insert_logs_res.data) > 0, "Service role should bypass RLS and insert log data"

    # 3. Cleanup analysis logs (Delete the tests record)
    delete_logs_res = service_client.table("analysis_logs").delete().eq("ticker", TEST_TICKER).execute()
    assert len(delete_logs_res.data) > 0, "Service role should be able to cleanup log tests data"

    delete_stock_res = service_client.table("stocks").delete().eq("ticker", TEST_TICKER).execute()
    assert len(delete_stock_res.data) > 0, "Service role should be able to cleanup stock tests data"


def test_public_can_read():
    """
    Scenario: Verify that the public can still read data (Select Policy).
    Expected: Success.
    """
    anon_client = db_manager.client
    # Check the 'stocks' table which should have public read access
    response = anon_client.table("stocks").select("*").limit(1).execute()


    assert response.data is not None, "Public should have read access to stocks table"