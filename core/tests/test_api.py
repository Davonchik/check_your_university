import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.application.services.admin_service import AdminService
from src.factories import admin_service_factory
from src.infrastructure.database.models.building import Building


client = TestClient(app)

@pytest.mark.asyncio
async def test_user(mocker):
    mock_service = mocker.MagicMock(spec=AdminService)
    mock_service.get_buildings.return_value = [
        Building(id = 1, name="pokra"),
        Building(id = 2, name="test"),
    ]

    app.dependency_overrides[admin_service_factory] = lambda: mock_service
    
    response = client.get("/user/get-buildings")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == ["pokra", "test"]