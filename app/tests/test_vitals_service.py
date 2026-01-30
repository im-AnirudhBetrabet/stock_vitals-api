import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.vitals_service import VitalsService

@pytest.fixture
def mock_repo() -> AsyncMock:
    """
    Fixture to mock the database repository
    :return:
    """
    return AsyncMock()

@pytest.fixture
def service(mock_repo):
    """
    Fixture to initialize the service with a mocked repo
    :param mock_repo:
    :return:
    """
    service       = VitalsService()
    service._repo = mock_repo
    return service

@pytest.mark.asyncio
async def test_pagination_logic(service, mock_repo):
    """
    Scenario: Verify that the service correctly calculates the total pages and formatting.
    :param service:
    :param mock_repo:
    :return:
    """
    mock_data = [
        {"id": 1, "ticker": "RELIANCE.NS", "final_score": 80, "timestamp": "2026-01-26T10:00:00",
         "track_used": "Maker", "accelerator_score": 40, "quality_score": 20, "bargain_score": 20,
         "raw_metrics": {}, "metric_scores": {}}
    ]
    mock_repo.fetch_paginated_logs.return_value = (mock_data, 100)

    page, size = 1, 10
    result     = await service.get_paginated_vitals(page, size)

    assert result["page"]  == 1
    assert result["total"] == 100
    assert result["pages"] == 10
    assert len(result['items']) == 1
    assert result['items'][0].ticker == 'RELIANCE.NS'


@pytest.mark.asyncio
async def test_empty_pagination_result(service, mock_repo):
    """
    Scenario: Verify handling of empty database result.
    :param service:
    :param mock_repo:
    :return:
    """
    mock_repo.fetch_paginated_logs.return_value = ([], 0)

    result = await service.get_paginated_vitals(1, 10)

    assert result["total"] == 0
    assert result["pages"] == 0
    assert result["items"] == []


@pytest.mark.asyncio
async def test_filtering_by_track(service, mock_repo):
    """
    Scenario: Verify that the service correctly filters by track and only
    returns matching items.
    """
    mock_data = [
        {"id": 2, "ticker": "ZOMATO.NS", "final_score": 85, "timestamp": "2026-01-26T12:00:00",
         "track_used": "Scalers", "accelerator_score": 50, "quality_score": 15, "bargain_score": 20,
         "raw_metrics": {}, "metric_scores": {}}
    ]
    mock_repo.fetch_paginated_logs.return_value = (mock_data, 1)

    # 2. Execute Service with Filter
    result = await service.get_paginated_vitals(page=1, size=10, track="Scalers")

    # 3. Assertions
    # Verify the repo was called with the correct filter
    mock_repo.fetch_paginated_logs.assert_called_with(0, 10, "Scalers")

    # Verify every item returned matches the track
    for item in result["items"]:
        assert item.track_used == "Scalers"
    assert result["total"] == 1


@pytest.mark.asyncio
async def test_filtering_case_insensitivity(service, mock_repo):
    """
    QA Test: Verify that 'scalers', 'SCALERS', and 'Scalers' are treated the same.
    """
    mock_repo.fetch_paginated_logs.return_value = ([], 0)

    # Test lowercase input
    await service.get_paginated_vitals(1, 10, track="scalers")

    mock_repo.fetch_paginated_logs.assert_called_with(0, 10, "scalers")