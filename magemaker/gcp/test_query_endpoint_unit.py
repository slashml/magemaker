import pytest
from unittest.mock import patch, MagicMock
from magemaker.gcp.query_endpoint import query_vertexai_endpoint_rest

@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    return {
        'PROJECT_ID': 'test-project',
        'GCLOUD_REGION': 'us-central1'
    }

@pytest.fixture
def mock_credentials():
    """Mock Google credentials."""
    mock_creds = MagicMock()
    mock_creds.token = 'test-token'
    return mock_creds

def test_query_endpoint_success(mock_env_vars, mock_credentials):
    """Test successful endpoint query."""
    with patch('magemaker.gcp.query_endpoint.dotenv_values') as mock_dotenv, \
         patch('google.auth.default') as mock_auth_default, \
         patch('requests.post') as mock_post:
        
        # Setup mocks
        mock_dotenv.return_value = mock_env_vars
        mock_auth_default.return_value = (mock_credentials, 'test-project')
        
        mock_response = MagicMock()
        mock_response.content = b'{"predictions": ["test result"]}'
        mock_response.json.return_value = {"predictions": ["test result"]}
        mock_post.return_value = mock_response
        
        # Test query
        result = query_vertexai_endpoint_rest(
            endpoint_id='test-endpoint',
            input_text='test input'
        )
        
        # Verify results
        assert result == {"predictions": ["test result"]}
        
        # Verify API call
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Verify URL
        expected_url = "https://us-central1-aiplatform.googleapis.com/v1/projects/test-project/locations/us-central1/endpoints/test-endpoint:predict"
        assert args[0] == expected_url
        
        # Verify headers
        assert kwargs['headers']['Authorization'] == 'Bearer test-token'
        assert kwargs['headers']['Content-Type'] == 'application/json'
        
        # Verify payload
        assert 'instances' in kwargs['json']
        assert kwargs['json']['instances'][0]['inputs'] == 'test input'

def test_query_endpoint_with_token_path(mock_env_vars, mock_credentials):
    """Test query with token path."""
    with patch('magemaker.gcp.query_endpoint.dotenv_values') as mock_dotenv, \
         patch('google.auth.load_credentials_from_file') as mock_load_creds, \
         patch('requests.post') as mock_post:
        
        # Setup mocks
        mock_dotenv.return_value = mock_env_vars
        mock_load_creds.return_value = (mock_credentials, 'test-project')
        
        mock_response = MagicMock()
        mock_response.content = b'{"predictions": ["test result"]}'
        mock_response.json.return_value = {"predictions": ["test result"]}
        mock_post.return_value = mock_response
        
        # Test query with token path
        result = query_vertexai_endpoint_rest(
            endpoint_id='test-endpoint',
            input_text='test input',
            token_path='path/to/token.json'
        )
        
        # Verify credential loading
        mock_load_creds.assert_called_once_with('path/to/token.json')
        
        assert result == {"predictions": ["test result"]}