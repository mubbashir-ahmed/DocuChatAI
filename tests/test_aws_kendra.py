import pytest
from unittest.mock import MagicMock, patch
from src.services.aws_kendra import AWSKendra

@patch('boto3.client')
@patch('src.configs.settings.settings.get_aws_kendra_index_id')
@patch('src.configs.settings.settings.get_aws_region')
@patch('src.configs.settings.settings.get_aws_access_key')
@patch('src.configs.settings.settings.get_aws_secret_key')
def test_get_kendra_query_results_success(mock_secret, mock_access, mock_region, mock_index_id, mock_boto_client):
    # Setup mocks
    mock_index_id.return_value = "index-id-123"
    mock_kendra_client = MagicMock()
    mock_boto_client.return_value = mock_kendra_client
    
    # Mock Kendra response
    mock_response = {
        'QueryId': 'qid-123',
        'ResultItems': [{'Id': 'item1'}]
    }
    mock_kendra_client.query.return_value = mock_response

    # Test
    kendra = AWSKendra.get_instance()
    # Reset singleton to ensure client is re-created (optional but safer)
    # But since it's lazy loaded in the method, mocking boto3.client is enough
    
    qid, items = kendra.get_kendra_query_results("test query")

    # Assertions
    assert qid == 'qid-123'
    assert items == [{'Id': 'item1'}]
    mock_kendra_client.query.assert_called_with(QueryText="test query", IndexId="index-id-123")

def test_get_answers_from_query_results_empty():
    kendra = AWSKendra.get_instance()
    answers = kendra.get_answers_from_query_results(None)
    assert answers == []
    answers = kendra.get_answers_from_query_results([])
    assert answers == []

def test_get_answers_from_query_results_mixed():
    kendra = AWSKendra.get_instance()
    
    # Construct mock result items
    # Item 1: ANSWER type
    item1 = {
        'Type': 'ANSWER',
        'DocumentURI': 'http://doc1',
        'ScoreAttributes': {'ScoreConfidence': 'VERY HIGH'},
        'DocumentExcerpt': {'Text': 'This is answer 1.'}
    }
    # Item 2: DOCUMENT type
    item2 = {
        'Type': 'DOCUMENT',
        'DocumentURI': 'http://doc2',
        'ScoreAttributes': {'ScoreConfidence': 'MEDIUM'},
        'DocumentExcerpt': {'Text': 'This.\nIs.\nDoc 2.'}
    }
    
    result_items = [item1, item2]
    
    answers = kendra.get_answers_from_query_results(result_items)

    assert len(answers) == 2

    # Check Answer 1 (VERY_HIGH should be 10)
    assert answers[0][0] == "This is answer 1."
    assert answers[0][1] == "http://doc1"
    assert answers[0][2] == 10  # Deterministic check

    # Check Answer 2 (MEDIUM should be 5)
    assert "This" in answers[1][0]
    assert answers[1][1] == "http://doc2"
    assert answers[1][2] == 5  # Deterministic check
