import json
import pytest
from unittest.mock import MagicMock, patch
from src.services.openai import OpenAI

@patch('src.services.openai.OpenAIClient')
def test_get_chatgpt_response_success(mock_openai_client_class):
    # Mock the OpenAI client instance
    mock_client = MagicMock()
    mock_openai_client_class.return_value = mock_client
    
    # Mock the chat completion response (new v2 API structure)
    mock_message = MagicMock()
    mock_message.content = "Generated response"
    
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    
    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    
    mock_client.chat.completions.create.return_value = mock_response
    
    openai_service = OpenAI.get_instance()
    response = openai_service.get_chatgpt_response(
        "prompt", 0.5, response_format={"type": "json_object"}
    )
    
    assert response == "Generated response"
    mock_client.chat.completions.create.assert_called_once()

@patch('src.services.openai.OpenAI.get_chatgpt_response')
def test_get_consensus_list_logic(mock_get_response):
    openai_service = OpenAI.get_instance()
    
    # Case 1: List logic
    # "The answers are items"
    # "0 | ['Item A', 'Item B']"
    # "1 | ['Item A']"
    # Weights: [10, 5]
    
    mock_data = {
        'type': 'items',
        'data': [
            {'id': 0, 'items': ['Item A', 'Item B']},
            {'id': 1, 'items': ['Item A']},
        ],
    }
    
    mock_get_response.return_value = json.dumps(mock_data)
    
    statements = ["s1", "s2"]
    weights = [10, 5]
    
    result = openai_service.get_consensus(statements, weights, "query")
    
    # Expected:
    # Item A: 10 + 5 = 15
    # Item B: 10
    
    assert result['Item A'] == 15
    assert result['Item B'] == 10

@patch('src.services.openai.OpenAI.get_chatgpt_response')
def test_get_consensus_statement_logic(mock_get_response):
    openai_service = OpenAI.get_instance()
    
    # Case 2: Statement logic
    # "The answer is a statement"
    # "Unified statement text"
    
    mock_data ={
        'type': 'statement',
        'text': 'This is the unified answer.',
    }
    
    mock_get_response.return_value = json.dumps(mock_data)
    
    statements = ["s1", "s2"]
    weights = [10, 5]
    
    result = openai_service.get_consensus(statements, weights, "query")
    
    # Expected:
    # "This is the unified answer.": sum(weights) = 15
    
    assert result['This is the unified answer.'] == 15
