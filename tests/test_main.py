import pytest
from unittest.mock import MagicMock, patch
from src.main import get_response_from_bot

@patch('src.main.AWSKendra')
@patch('src.main.OpenAI')
def test_get_response_from_bot_success(mock_openai, mock_aws_kendra):
    # Setup Mock for AWSKendra
    mock_kendra_instance = MagicMock()
    mock_aws_kendra.get_instance.return_value = mock_kendra_instance
    
    # Mock return values for Kendra
    query_id = "test-query-id"
    result_items = [{"some": "item"}]
    mock_kendra_instance.get_kendra_query_results.return_value = (query_id, result_items)
    
    # Mock answers from Kendra
    # Each item is [answer_text, url, confidence_score]
    answers_with_urls = [
        ["Answer 1", "http://url1.com", 10],
        ["Answer 2", "http://url2.com", 8]
    ]
    mock_kendra_instance.get_answers_from_query_results.return_value = answers_with_urls
    
    # Setup Mock for OpenAI
    mock_openai_instance = MagicMock()
    mock_openai.get_instance.return_value = mock_openai_instance
    
    # Mock consensus result
    consensus_result = {"Final Answer": 18} # 10 + 8
    mock_openai_instance.get_consensus.return_value = consensus_result
    
    # Run function
    query = "test query"
    response = get_response_from_bot(query)
    
    # Assertions
    assert response is not None
    assert response[0].queryId == query_id
    assert response[0].answer == "Final Answer"
    assert response[0].score == 18
    assert response[0].urls == ["http://url1.com", "http://url2.com"]


@patch('src.main.AWSKendra')
@patch('src.main.OpenAI')
def test_get_response_from_bot_multiple_results(mock_openai, mock_aws_kendra) -> None:
    """New test to verify that multiple consensus answers are returned correctly."""
    
    mock_kendra_instance = MagicMock()
    mock_aws_kendra.get_instance.return_value = mock_kendra_instance
    mock_kendra_instance.get_kendra_query_results.return_value = ("qid", [])
    mock_kendra_instance.get_answers_from_query_results.return_value = []
    
    mock_openai_instance = MagicMock()
    mock_openai.get_instance.return_value = mock_openai_instance

    # Mock two consensus results
    consensus_result = {"Answer A": 10, "Answer B": 5}
    
    mock_openai_instance.get_consensus.return_value = consensus_result

    response = get_response_from_bot("query")

    assert isinstance(response, list)
    assert len(response) == 2
    assert response[0].answer == "Answer A"
    assert response[1].answer == "Answer B"


@patch('src.main.AWSKendra')
@patch('src.main.OpenAI')
def test_get_response_from_bot_no_consensus(mock_openai, mock_aws_kendra):
    # Setup Mock for AWSKendra
    mock_kendra_instance = MagicMock()
    mock_aws_kendra.get_instance.return_value = mock_kendra_instance
    
    mock_kendra_instance.get_kendra_query_results.return_value = ("qid", [])
    mock_kendra_instance.get_answers_from_query_results.return_value = []
    
    # Setup Mock for OpenAI
    mock_openai_instance = MagicMock()
    mock_openai.get_instance.return_value = mock_openai_instance
    mock_openai_instance.get_consensus.return_value = {} # No consensus
    
    # Run function
    response = get_response_from_bot("query")
    
    # Assertions
    assert response == []
