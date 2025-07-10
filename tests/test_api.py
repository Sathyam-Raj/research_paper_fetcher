import pytest # type: ignore
from unittest.mock import patch
from paperfetcher.api import search_papers, fetch_paper_details

@patch("requests.get")
def test_search_papers_success(mock_get):
    mock_response = {
        "esearchresult": {
            "idlist": ["123456", "789012"]
        }
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    
    result = search_papers("cancer")
    assert result == ["123456", "789012"]

@patch("requests.get")
def test_search_papers_failure(mock_get):
    mock_get.return_value.status_code = 404
    result = search_papers("cancer")
    assert result == []

@patch("requests.get")
def test_fetch_paper_details_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<xml>test content</xml>"
    
    result = fetch_paper_details("123456")
    assert result == "<xml>test content</xml>"

@patch("requests.get")
def test_fetch_paper_details_failure(mock_get):
    mock_get.return_value.status_code = 404
    result = fetch_paper_details("123456")
    assert result is None