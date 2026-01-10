import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.api import app
from src.models.chatbot_response import ChatbotResponse

client = TestClient(app)

@patch('src.api.get_response_from_bot')
@patch('src.api.csv_logger')
def test_chatbot_endpoint_success(mock_logger, mock_get_response):
    # Setup mock response
    mock_response = ChatbotResponse(
        queryId="job-123",
        answer="Test Answer",
        score=100,
        urls=["http://test.com"]
    )
    mock_get_response.return_value = mock_response

    # Make request
    payload = {"query": "Hello"}
    response = client.post("/chatbot", json=payload)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["queryId"] == "job-123"
    assert data["answer"] == "Test Answer"
    assert data["urls"] == ["http://test.com"]

@patch('src.api.csv_logger')
def test_chatbot_endpoint_empty_query(mock_logger):
    # Make request with empty query
    payload = {"query": ""}
    response = client.post("/chatbot", json=payload)

    # Assertions
    assert response.status_code == 400
    assert response.json()["detail"] == "Empty query."

@patch('src.api.csv_logger')
def test_chatbot_endpoint_validation_error(mock_logger):
    # Make request with missing field
    payload = {}
    response = client.post("/chatbot", json=payload)

    # Assertions
    assert response.status_code == 422 # Validation Error

@patch('src.api.get_response_from_bot')
@patch('src.api.csv_logger')
def test_chatbot_endpoint_not_found(mock_logger, mock_get_response):
    # Setup mock to return None (no answer)
    mock_get_response.return_value = None

    # Make request
    payload = {"query": "Unknown question"}
    response = client.post("/chatbot", json=payload)

    # Assertions
    assert response.status_code == 404
    assert response.json()["detail"] == "No answer found for your query."

@patch('src.api.get_response_from_bot')
@patch('src.api.csv_logger')
def test_chatbot_endpoint_internal_error(mock_logger, mock_get_response):
    # Setup mock to raise exception
    mock_get_response.side_effect = Exception("Crash")

    # Make request
    payload = {"query": "Crash me"}
    response = client.post("/chatbot", json=payload)

    # Assertions
    # Should be caught by global exception handler => 500
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal Server Error"
