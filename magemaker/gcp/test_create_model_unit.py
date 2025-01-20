import pytest
from unittest.mock import patch, MagicMock
from magemaker.gcp.create_model import deploy_huggingface_model_to_vertexai
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource

@pytest.fixture
def sample_config():
    """Create sample configs for testing."""
    model = Model(
        id="distilbert-base-uncased",
        source=ModelSource.HuggingFace
    )
    deployment = Deployment(
        destination="gcp",
        instance_type="n1-standard-4",
        instance_count=1
    )
    return model, deployment

@pytest.mark.unit
def test_successful_deployment(sample_config):
    """Test successful model deployment."""
    model, deployment = sample_config
    
    # Mock the environment variables
    with patch('magemaker.gcp.create_model.dotenv_values') as mock_env:
        mock_env.return_value = {
            "GCLOUD_REGION": "us-central1",
            "PROJECT_ID": "test-project"
        }
        
        # Mock the deployment function
        with patch('magemaker.gcp.create_model._deploy_model') as mock_deploy:
            mock_endpoint = MagicMock()
            mock_deploy.return_value = mock_endpoint
            
            # Test the deployment
            result = deploy_huggingface_model_to_vertexai(deployment, model)
            assert result == mock_endpoint
            mock_deploy.assert_called_once()

@pytest.mark.unit
def test_failed_deployment(sample_config):
    """Test handling of deployment failure."""
    model, deployment = sample_config
    
    # Mock the environment variables
    with patch('magemaker.gcp.create_model.dotenv_values') as mock_env:
        mock_env.return_value = {
            "GCLOUD_REGION": "us-central1",
            "PROJECT_ID": "test-project"
        }
        
        # Mock the deployment function to raise an error
        with patch('magemaker.gcp.create_model._deploy_model') as mock_deploy:
            mock_deploy.side_effect = Exception("Deployment failed")
            
            # Test that the error is handled
            try:
                deploy_huggingface_model_to_vertexai(deployment, model)
            except Exception as e:
                assert str(e) == "Deployment failed"