import pytest
from unittest.mock import AsyncMock
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
async def test_search_tickers_min_length(service):
    """
    Verify that search returns an empty list if query is too short.
    """
    # Should not even call the repository
    result = await service.search_tickers("n")
    assert result == []


@pytest.mark.asyncio
async def test_search_tickers_success(service, mock_repo):
    """
    Verify that valid queries return the expected stock metadata.
    """
    mock_repo.search_stocks.return_value = [
        {"ticker": "NIVABUPA.NS", "name": "Niva Bupa Health Insurance"}
    ]

    result = await service.search_tickers("niva")

    assert len(result) == 1
    assert result[0]["ticker"] == "NIVABUPA.NS"
    mock_repo.search_stocks.assert_called_once_with("niva")