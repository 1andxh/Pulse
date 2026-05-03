import pytest
from httpx import AsyncClient, ASGITransport
from src.db.session import get_session
from src import app
from tests.test_database import db_session


@pytest.mark.asyncio
async def test_create_monitor_Api(db_session):
    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test/") as client:
        response = await client.post(
            "/",
            json={
                "name": "Test Monitor",
                "url": "https://example.com",
                "check_interval": 10,
            },
        )
        assert response.status_code == 201

        data = response.json()
        assert data["url"] == "https://example.com"
        assert data["name"] == "Test Monitor"
        assert "id" in data

        app.dependency_overrides.clear()
