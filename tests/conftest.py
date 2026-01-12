"""Shared test fixtures for the ChatOps test suite."""

import pytest
from fastapi.testclient import TestClient
from app.main import server


@pytest.fixture(scope="module")
def api_client():
    """Provide a TestClient bound to the FastAPI server."""
    with TestClient(server) as client:
        yield client
