import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.schemas import UserQuery, BotResponse

# Mock the RAG_ENGINE for testing
@pytest.fixture
def mock_rag_engine():
    with patch('backend.app.main.RAG_ENGINE') as mock:
        mock.query.return_value = ["Test context about coffee"]
        yield mock

@pytest.fixture
def client():
    return TestClient(app)

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch('backend.app.api.get_llm')
def test_api_non_spanish_question(mock_get_llm, client, mock_rag_engine):
    """Test that non-Spanish questions are rejected"""
    response = client.post("/ask", json={"question": "How do I make a latte?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Solo hablo español."
    assert data["retries"] == 0
