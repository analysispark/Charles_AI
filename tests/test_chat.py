import pytest
from unittest.mock import Mock, patch
from backend.chat import ChatRequest, ChatResponse
from backend.ollama_client import OllamaClient

def test_chat_request_model():
    """Test that ChatRequest model works correctly"""
    request = ChatRequest(message="Hello")
    assert request.message == "Hello"

def test_chat_response_model():
    """Test that ChatResponse model works correctly"""
    response = ChatResponse(response="Hi there!")
    assert response.response == "Hi there!"

@patch('requests.post')
def test_ollama_client_send_message_success(mock_post):
    """Test successful message sending to Ollama"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Hello from Ollama!"}
    mock_post.return_value = mock_response
    
    client = OllamaClient()
    result = client.send_message("test message")
    
    assert result == "Hello from Ollama!"
    mock_post.assert_called_once()

@patch('requests.post')
def test_ollama_client_send_message_error(mock_post):
    """Test error handling in Ollama client"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_post.return_value = mock_response
    
    client = OllamaClient()
    
    with pytest.raises(Exception):
        client.send_message("test message")
