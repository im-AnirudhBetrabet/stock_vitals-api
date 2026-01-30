from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_search_endpoint_contract():
    """
    Verify the HTTP response structure for the search endpoint.
    """
    # Use the TestClient to hit the actual URL
    response = client.get("/api/v1/search/stocks?query=niva")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_endpoint_validation_error():
    """
    Verify that the API returns a 422 error if the query is missing.
    """
    response = client.get("/api/v1/search/stocks")  # Missing 'q' param
    assert response.status_code == 422