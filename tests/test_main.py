"""Tests for the main FastAPI endpoints."""


class TestHealthCheck:
    """Verify the health-check and status routes."""

    def test_root_returns_200(self, api_client):
        resp = api_client.get("/")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "healthy"

    def test_status_endpoint(self, api_client):
        resp = api_client.get("/status")
        assert resp.status_code == 200
        body = resp.json()
        assert "version" in body
        assert "environment" in body


class TestChatEndpoint:
    """Verify the /chat endpoint."""

    def test_empty_message_returns_400(self, api_client):
        resp = api_client.post("/chat", json={"message": ""})
        assert resp.status_code == 400

    def test_valid_message_returns_intent(self, api_client):
        resp = api_client.post("/chat", json={"message": "I need help"})
        assert resp.status_code == 200
        body = resp.json()
        assert "intent" in body
        assert "response" in body
