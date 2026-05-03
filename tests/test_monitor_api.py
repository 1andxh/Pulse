import pytest
from sqlalchemy import select
from src.monitor.models import Monitor
import asyncio
from src import app


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
async def test_create_monitor_duplicate(db_session, client):
    payload = {
        "name": "Test Monitor",
        "url": "https://example.com",
        "check_interval": 10,
    }
    response1 = await client.post("/", json=payload)
    assert response1.status_code == 201

    response2 = await client.post("/", json=payload)
    assert response2.status_code == 409


@pytest.mark.asyncio
async def test_create_monitor_race_condition(db_session, client):
    payload = {
        "name": "Test-race-Monitor",
        "url": "https://example.com",
        "check_interval": 30,
    }

    async def send_request():
        return await client.post("/", json=payload)

    responses = await asyncio.gather(
        send_request(), send_request(), return_exceptions=True
    )

    success = [
        r for r in responses if hasattr(r, "status_code") and r.status_code == 201  # type: ignore
    ]

    failures = [
        r for r in responses if hasattr(r, "status_code") and r.status_code != 201  # type: ignore
    ]

    assert len(success) <= 1, f"Expected success, got {len(success)}"
    assert len(failures) == 1, f"Expected 1 failure, got {len(failures)}"
