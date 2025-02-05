import pytest
from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

client = TestClient(app)

def test_user(mocker):
    mock_db = mocker.MagicMock(spec=Session)
    mock_building = MagicMock()
    mock_building.name = "pokra"
    mock_building.id = 1
    mock_db.query.return_value.filter.return_value.first.return_value = mock_building
    mocker.patch("src.factories.session_factory", return_value=mock_db)
    response = client.get("/user/get-buildings")
    assert response.status_code == 200
    assert response.json() == []
