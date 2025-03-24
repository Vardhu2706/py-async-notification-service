import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_valid_email_notification():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "type": "email",
            "to": "test@example.com",
            "subject": "Test Email",
            "body": "Testing email payload."
        }
        response = await ac.post("/notify/", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "queued"


@pytest.mark.asyncio
async def test_valid_sms_notification():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "type": "sms",
            "to": "+1234567890",
            "body": "Test SMS message"
        }
        response = await ac.post("/notify/", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "queued"


@pytest.mark.asyncio
async def test_missing_body_field():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "type": "email",
            "to": "test@example.com",
            "subject": "Missing body"
        }
        response = await ac.post("/notify/", json=payload)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_missing_to_field():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "type": "push",
            "subject": "Missing to",
            "body": "Oops"
        }
        response = await ac.post("/notify/", json=payload)
        assert response.status_code == 422
