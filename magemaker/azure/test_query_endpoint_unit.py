
import pytest
from unittest.mock import patch, MagicMock
from magemaker.azure.query_endpoint import query_azure_endpoint

@pytest.fixture
def mock_env_vars():
    return {
        "AZURE_SUBSCRIPTION_ID": "test-sub",
        "AZURE_RESOURCE_GROUP": "test-group",
        "AZURE_WORKSPACE_NAME": "test-workspace"
    }

def test_query_endpoint_success(mock_env_vars):
    with patch('magemaker.azure.query_endpoint.dotenv_values') as mock_dotenv, \
         patch('magemaker.azure.query_endpoint.DefaultAzureCredential') as mock_cred, \
         patch('magemaker.azure.query_endpoint.MLClient') as mock_ml_client, \
         patch('builtins.open'), \
         patch('json.dump'), \
         patch('os.remove'):
        
        # Setup mocks
        mock_dotenv.return_value = mock_env_vars  # Fixed typo here
        mock_client = MagicMock()
        mock_ml_client.return_value = mock_client
        mock_client.online_endpoints.invoke.return_value = {"result": "test response"}
        
        # Test endpoint query
        result = query_azure_endpoint("test-endpoint", "test query")
        
        # Verify result
        assert result == {"result": "test response"}
        
        # Verify endpoint was invoked with correct parameters
        mock_client.online_endpoints.invoke.assert_called_once()
        args = mock_client.online_endpoints.invoke.call_args
        assert args[1]['endpoint_name'] == "test-endpoint"