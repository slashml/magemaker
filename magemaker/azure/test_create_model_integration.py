import os
import pytest
from dotenv import load_dotenv

from magemaker.azure.create_model import deploy_huggingface_model_to_azure
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource

# Load environment variables
load_dotenv()

def test_model_deployment():
    """
    Test deployment of an model
    """
    # Ensure we have the required environment variables
    required_vars = ['AZURE_SUBSCRIPTION_ID', 'AZURE_RESOURCE_GROUP', 'AZURE_WORKSPACE_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        pytest.skip(f"Missing environment variables: {missing_vars}")
    
    # Create an model
    test_model = Model(
        id="non-existent-model-xyz",
        source=ModelSource.HuggingFace
    )
    
    # Create deployment configuration
    deployment = Deployment(
        destination="azure",
        instance_type="Standard_DS3_v2",
        instance_count=1
    )
    
    # Expect deployment to fail for model
    with pytest.raises((Exception, SystemExit)):
        deploy_huggingface_model_to_azure(deployment, test_model)