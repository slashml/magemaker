import pytest
import boto3
import time
from magemaker.sagemaker.create_model import deploy_huggingface_model_to_sagemaker
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource
from magemaker.session import session

@pytest.fixture(scope="module")
def sagemaker_client():
    """Create a SageMaker client for testing."""
    return boto3.client('sagemaker', region_name=session.region_name)

@pytest.mark.integration
def test_deploy_simple_huggingface_model(sagemaker_client):
    """Test deploying a simple HuggingFace model to SageMaker."""
    try:
        # Use a small, simple model for testing
        model = Model(
            id="distilbert-base-uncased",  # Small model for faster testing
            source=ModelSource.HuggingFace
        )
        
        # Use minimal deployment configuration
        deployment = Deployment(
            destination="aws",
            instance_type="ml.t2.medium",  # Small instance for testing
            instance_count=1
        )
        
        # Deploy the model
        predictor = deploy_huggingface_model_to_sagemaker(deployment, model)
        
        # Wait for endpoint to be ready (with shorter timeout)
        waiter = sagemaker_client.get_waiter('endpoint_in_service')
        waiter.wait(
            EndpointName=predictor.endpoint_name,
            WaiterConfig={'Delay': 30, 'MaxAttempts': 20}
        )
        
        # Verify endpoint exists and is running
        response = sagemaker_client.describe_endpoint(
            EndpointName=predictor.endpoint_name
        )
        assert response['EndpointStatus'] == 'InService'
        
        # Cleanup
        sagemaker_client.delete_endpoint(EndpointName=predictor.endpoint_name)
        print(f"Successfully deployed and cleaned up endpoint: {predictor.endpoint_name}")
        
    except Exception as e:
        # If any endpoint was created, try to clean it up
        if 'predictor' in locals() and hasattr(predictor, 'endpoint_name'):
            try:
                sagemaker_client.delete_endpoint(EndpointName=predictor.endpoint_name)
            except:
                pass
        pytest.fail(f"Test failed with error: {str(e)}")