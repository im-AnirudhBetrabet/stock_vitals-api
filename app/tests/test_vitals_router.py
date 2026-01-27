from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_get_all_vitals_endpoint():
    """
    Scenario: Verify whether the router returns a 200 and the correct JSON structure
    :return:
    """

    response = client.get("/api/v1/vitals/all?page=1&size=5")
    assert response.status_code == 200
    json_data = response.json()

    assert "items" in json_data
    assert "total" in json_data
    assert "pages" in json_data
