from unittest.mock import MagicMock, patch
import pytest

from tags_provider import HttpTagsProvider

@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get

def test_fetch_service_tag_map_lists(mock_requests_get):
    mock_response = MagicMock()
    mock_response.text = '{"service1": {"tag1": ["value1", "value2"]}, "service2": {"tag2": ["value3"]}}'
    mock_requests_get.return_value = mock_response

    provider = HttpTagsProvider("http://example.com/tags")
    service_tag_map_lists = provider._HttpTagsProvider__fetch_service_tag_map_lists()
    assert service_tag_map_lists == {'service1': {'tag1': ['value1', 'value2']}, 'service2': {'tag2': ['value3']}}
    
def test_refresh_service_tags(mock_requests_get):
    mock_response = MagicMock()
    mock_response.text = '{"service1": {"tag1": ["value1", "value2"]}, "service2": {"tag2": ["value3"]}}'
    mock_requests_get.return_value = mock_response

    provider = HttpTagsProvider("http://example.com/tags")
    provider._HttpTagsProvider__refresh_service_tags()
    assert provider.service_tags == {'service1': [{'tag1': 'value1'}, {'tag1': 'value2'}], 'service2': [{'tag2': 'value3'}]}

def test_get_service_tags(mock_requests_get):
    mock_response = MagicMock()
    mock_response.text = '{"service1": {"tag1": ["value1", "value2"]}, "service2": {"tag2": ["value3"]}}'
    mock_requests_get.return_value = mock_response

    provider = HttpTagsProvider("http://example.com/tags")
    service_tags = provider.get_service_tags()
    assert service_tags == {'service1': [{'tag1': 'value1'}, {'tag1': 'value2'}], 'service2': [{'tag2': 'value3'}]}
