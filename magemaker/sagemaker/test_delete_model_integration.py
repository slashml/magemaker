import pytest
import boto3
import time
from magemaker.sagemaker.create_model import deploy_huggingface_model_to_sagemaker
from magemaker.sagemaker.delete_model import delete_sagemaker_model
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource
from magemaker.session import session

@pytest.fixture(scope="module")
def sagemaker_client():
    """Create a SageMaker client for testing."""
    return boto3.client('sagemaker', region_name=session.region_name)

@pytest.mark.integration
def test_delete_model(sagemaker_client):
    """Test end-to-end model deployment and deletion."""
    # Create and deploy a model
    model = Model(
        id="distilbert-base-uncased",
        source=ModelSource.HuggingFace
    )
    deployment = Deployment(
        destination="aws",
        instance_type="ml.t2.medium",
        instance_count=1
    )

    try:
        # Deploy model
        print("Deploying model...")
        predictor = deploy_huggingface_model_to_sagemaker(deployment, model)
        endpoint_name = predictor.endpoint_name
        print(f"Model deployed to endpoint: {endpoint_name}")

        # Wait for endpoint to be ready
        waiter = sagemaker_client.get_waiter('endpoint_in_service')
        waiter.wait(EndpointName=endpoint_name, WaiterConfig={'Delay': 30, 'MaxAttempts': 20})
        print("Endpoint is ready")

        # Delete the endpoint
        print("Deleting endpoint...")
        delete_sagemaker_model([endpoint_name])

        # Verify deletion
        time.sleep(30)  # Give some time for deletion to complete
        with pytest.raises(Exception) as e:
            sagemaker_client.describe_endpoint(EndpointName=endpoint_name)
        assert "Could not find endpoint" in str(e.value)
        print("Endpoint successfully deleted")

    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")