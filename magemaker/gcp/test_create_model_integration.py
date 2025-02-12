import pytest
import os
from google.cloud import aiplatform
from magemaker.gcp.create_model import deploy_huggingface_model_to_vertexai
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource
from dotenv import load_dotenv

load_dotenv()
PROJECT_ID = os.getenv("PROJECT_ID")
GCLOUD_REGION = os.getenv("GCLOUD_REGION")

@pytest.fixture(scope="session", autouse=True)
def setup():
    """Initialize Vertex AI."""
    if not PROJECT_ID or not GCLOUD_REGION:
        pytest.skip("Environment variables not set")
    aiplatform.init(project=PROJECT_ID, location=GCLOUD_REGION)

@pytest.mark.integration
def test_create_and_deploy_gcp_model():
    """
    Test actual model creation and deployment with minimal configuration.
    Tests the core functionality of deploy_huggingface_model_to_vertexai.
    """
    # Test configurations
    model = Model(
        id="Qwen/CodeQwen1.5-7B-Chat",  # Using a small model
        source=ModelSource.HuggingFace
    )
    
    deployment = Deployment(
        destination="gcp",
        instance_type="n1-standard-4",
        instance_count=1,
        min_replica_count=1,
        max_replica_count=1
    )
    
    endpoint = None
    
    try:
        # Test actual model deployment
        print(f"\nAttempting model deployment...")
        endpoint = deploy_huggingface_model_to_vertexai(deployment, model)
        
        # Verify endpoint creation
        assert endpoint is not None
        assert endpoint.resource_name is not None
        print(f"Successfully deployed endpoint: {endpoint.resource_name}")
        
    except Exception as e:
        pytest.fail(f"Model deployment failed: {str(e)}")
        
    finally:
        # Cleanup
        if endpoint:
            try:
                print("\nCleaning up resources...")
                endpoint.undeploy_all()
                endpoint.delete()
                print("Cleanup completed")
            except Exception as e:
                print(f"Cleanup failed: {str(e)}")