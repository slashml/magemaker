from unittest.mock import patch
from magemaker.schemas.model import Model
from magemaker.schemas.deployment import Deployment
from magemaker.gcp.create_model import deploy_huggingface_model_to_vertexai
@patch('google.cloud.aiplatform.Model')
@patch('google.cloud.aiplatform.init')

def test_deploy_huggingface_model_to_vertexai(mock_init, mock_model):
    # Create a mock endpoint with resource_name attribute
    from unittest.mock import MagicMock
    mock_endpoint = MagicMock()
    mock_endpoint.resource_name = 'test_endpoint_resource'
    
    mock_model_instance = mock_model.upload.return_value
    mock_model_instance.deploy.return_value = mock_endpoint
    mock_model_instance.resource_name = 'test_resource_name'

    deployment = Deployment(
        endpoint_name="test-endpoint",
        instance_type="g2-standard-12",
        accelerator_type="NVIDIA_L4",
        destination="gcp",
        accelerator_count=1,
        quantization=None,
        num_gpus=None
    )

    model = Model(
        id="facebook/opt-125m",
        source="huggingface",
    )

    deploy_huggingface_model_to_vertexai(deployment=deployment, model=model)