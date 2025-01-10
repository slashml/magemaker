import pytest
from unittest.mock import patch, MagicMock
from azure.core.exceptions import ResourceNotFoundError
from magemaker.azure.delete_model import delete_azure_model

@pytest.fixture
def mock_env_vars():
    return {
        "AZURE_SUBSCRIPTION_ID": "test-sub",
        "AZURE_RESOURCE_GROUP": "test-group",
        "AZURE_WORKSPACE_NAME": "test-workspace"
    }

def test_delete_model_success(mock_env_vars):
    with patch('magemaker.azure.delete_model.dotenv_values') as mock_dotenv, \
         patch('magemaker.azure.delete_model.DefaultAzureCredential'), \
         patch('magemaker.azure.delete_model.MLClient') as mock_ml_client:
        
        mock_dotenv.return_value = mock_env_vars
        mock_client = MagicMock()
        mock_ml_client.return_value = mock_client
        
        result = delete_azure_model("test-endpoint")
        assert result is True
        mock_client.online_endpoints.begin_delete.assert_called_once()

def test_delete_nonexistent_model(mock_env_vars):
    with patch('magemaker.azure.delete_model.dotenv_values') as mock_dotenv, \
         patch('magemaker.azure.delete_model.DefaultAzureCredential'), \
         patch('magemaker.azure.delete_model.MLClient') as mock_ml_client:
        
        mock_dotenv.return_value = mock_env_vars
        mock_client = MagicMock()
        mock_client.online_endpoints.get.side_effect = ResourceNotFoundError("Not found")
        mock_ml_client.return_value = mock_client
        
        result = delete_azure_model("nonexistent-endpoint")
        assert result is False