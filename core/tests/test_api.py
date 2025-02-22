import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.application.services.admin_service import AdminService
from src.application.services.s3_service import S3Service
from src.application.services.request_service import RequestService
from src.factories import admin_service_factory, request_service_factory
from src.infrastructure.database.models.building import Building
from src.infrastructure.database.models.request import Request
from src.infrastructure.database.models.user import User
from src.application.domain.request import RequestCreate, RequestOut, RequestUpdate
import jwt
from datetime import datetime, timedelta

client = TestClient(app)

# User tests.

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

# Admin tests.

@pytest.mark.asyncio
async def test_login(mocker):
    mock_service = mocker.MagicMock(spec=AdminService)
    mock_service.login.return_value = {
        "email": "test",
        "access_token": "test",
        "refresh_token": "test"
    }

    app.dependency_overrides[admin_service_factory] = lambda: mock_service

    response = client.post("/admin/", json={"email": "test", "password": "test"})

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"email": "test", "access_token": "test", "refresh_token": "test"}
    

@pytest.mark.asyncio
async def test_refresh_token(mocker):
    mock_service = mocker.MagicMock(spec=AdminService)
    mock_service.refresh_token.return_value = {
        "email": "test",
        "access_token": "test",
        "refresh_token": "test"
    }

    app.dependency_overrides[admin_service_factory] = lambda: mock_service

    response = client.post("/admin/refresh", params={"refresh_token": "test"})

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"email": "test", "access_token": "test", "refresh_token": "test"}

# @pytest.mark.asyncio
# async def test_update_request(mocker):
#     mock_service = mocker.MagicMock()
#     mock_service.update_request.return_value = RequestUpdate(request_id=1,status="done")

#     app.dependency_overrides[RequestService] = lambda: mock_service

#     user = User(
#         id = 1,
#         tg_id = 1
#     )

#     req = Request(
#         id = 1,
#         user_id=1,
#         building_id=1,
#         category="test",
#         room="test",
#         text="test",
#         photo_url="test",
#         status="done",
#         user=user
#     )

#     # Мокаем decode_access_token, чтобы X-Auth-Token всегда был валиден
#     mocker.patch(
#         "src.infrastructure.utils.token_service.TokenService.decode_access_token",
#         return_value={"user_id": 1, "role": "admin"}
#     )
#     mocker.patch("src.infrastructure.utils.kafka_producer.KafkaProducer.send_message", return_value=None)
#     mocker.patch("src.infrastructure.database.dao.request_dao.RequestDao.update_request", return_value=req)


#     response = client.post(
#         "/admin_actions/update",
#         json={"request_id": 1, "status": "done"},  # В теле запроса остается только status
#         headers={"X-Auth-Token": "test_token"}  # Добавляем заголовок
#     )

#     app.dependency_overrides.clear()

#     assert response.status_code == 200
#     assert response.json() == {"status": "done"}



@pytest.mark.asyncio
async def test_get_requests(mocker):
    mock_service = mocker.MagicMock(spec=RequestService)
    mock_service.get_requests.return_value = [
        Request(id = 1, user_id=1, building_id=1, category="test", room="test", text="test"),
        Request(id = 2, user_id=2, building_id=1, category="test", room="test", text="test"),
    ]

    app.dependency_overrides[request_service_factory] = lambda: mock_service

    mocker.patch(
        "src.infrastructure.utils.token_service.TokenService.decode_access_token",
        return_value={"user_id": 1, "role": "admin"}
    )

    response = client.get(
        "/admin_actions/",
        headers={"X-Auth-Token": "test_token"})

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "user_id": 1, "building_id": 1, "category": "test", "room": "test", "text": "test"},
        {"id": 2, "user_id": 2, "building_id": 1, "category": "test", "room": "test", "text": "test"},
    ]

@pytest.mark.asyncio
async def test_create_building(mocker):
    mock_service = mocker.MagicMock(spec=AdminService)
    building = Building(
        id = 1, 
        name="test"
    )
    mock_service.create_building.return_value = building

    app.dependency_overrides[admin_service_factory] = lambda: mock_service
    
    mocker.patch(
        "src.infrastructure.utils.token_service.TokenService.decode_access_token",
        return_value={"user_id": 1, "role": "admin"}
    )

    response = client.post(
        "/admin_actions/create-building",
        headers={"X-Auth-Token": "test_token"},
        params={"name": "test"}
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "test"}

@pytest.mark.asyncio
async def test_delete_building(mocker):
    mock_service = mocker.MagicMock(spec=AdminService)
    building = Building(
        id = 1,
        name = 'test'
    )
    mock_service.delete_building.return_value = building

    app.dependency_overrides[admin_service_factory] = lambda: mock_service

    mocker.patch(
        "src.infrastructure.utils.token_service.TokenService.decode_access_token",
        return_value={"user_id": 1, "role": "admin"}
    )

    response = client.post(
        "/admin_actions/delete-building",
        headers={"X-Auth-Token": "test_token"},
        params={"id": 1}
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "test"}
