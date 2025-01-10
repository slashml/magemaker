import pytest
from unittest.mock import patch, MagicMock
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource

@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    return {
        "AZURE_SUBSCRIPTION_ID": "test-sub",
        "AZURE_RESOURCE_GROUP": "test-group",
        "AZURE_WORKSPACE_NAME": "test-workspace"
    }

@pytest.fixture
def sample_model():
    """Create sample model configuration."""
    return Model(
        id="bert-base-uncased",
        source=ModelSource.HuggingFace
    )

@pytest.fixture
def sample_deployment():
    """Create sample deployment configuration."""
    return Deployment(
        destination="azure",
        instance_type="Standard_DS3_v2",
        instance_count=1
    )

def test_deploy_model_to_azure(mock_env_vars, sample_model, sample_deployment):
    """Test the model deployment function."""
    with patch('magemaker.azure.create_model.dotenv_values') as mock_dotenv, \
         patch('magemaker.azure.create_model.DefaultAzureCredential') as mock_cred, \
         patch('magemaker.azure.create_model.MLClient') as mock_ml_client:
        
        # Setup mocks
        mock_dotenv.return_value = mock_env_vars
        mock_client = MagicMock()
        mock_ml_client.return_value = mock_client
        
        # Mock successful workspace access
        mock_workspace = MagicMock()
        mock_workspace.name = "test-workspace"
        mock_client.workspaces.get.return_value = mock_workspace
        
        # Mock endpoint creation
        mock_endpoint = MagicMock()
        mock_endpoint.scoring_uri = "https://test-endpoint"
        mock_client.begin_create_or_update.return_value.result.return_value = mock_endpoint
        
        from magemaker.azure.create_model import deploy_huggingface_model_to_azure
        
        # Test deployment
        result = deploy_huggingface_model_to_azure(sample_deployment, sample_model)
        
        # Verify basic interactions
        mock_ml_client.assert_called_once()
        mock_client.workspaces.get.assert_called_once()