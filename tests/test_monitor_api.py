import pytest
from sqlalchemy import select
from src.monitor.models import Monitor


@pytest.mark.asyncio
async def test_create_monitor_api(db_session, client):

    response = await client.post(
        "/",
        json={
            "name": "Test Monitor",
            "url": "https://example.com",
            "check_interval": 10,
        },
    )

    result = await db_session.execute(select(Monitor))
    monitors = result.scalars().all()

    assert len(monitors) == 1
    assert response.status_code == 201

    data = response.json()
    assert data["url"] == "https://example.com"
    assert data["name"] == "Test Monitor"
    assert "id" in data


@pytest.mark.asyncio
async def test_monitor_duplicate(db_session, client):
    response = await client.post(
        "/",
        json={
            "name": "Test Monitor",
            "url": "https://example.com",
            "check_interval": 10,
        },
    )
