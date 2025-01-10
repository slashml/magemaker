import os
import pytest
import uuid
from dotenv import load_dotenv

from magemaker.azure.delete_model import delete_azure_model
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.core.exceptions import ResourceNotFoundError

# Load environment variables
load_dotenv()

def test_delete_nonexistent_endpoint():
    """
    Test deleting a nonexistent endpoint
    """
    # Ensure we have the required environment variables
    required_vars = ['AZURE_SUBSCRIPTION_ID', 'AZURE_RESOURCE_GROUP', 'AZURE_WORKSPACE_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        pytest.skip(f"Missing environment variables: {missing_vars}")
    
    # Generate a random endpoint name that is unlikely to exist
    random_endpoint_name = "test-nonexistent-endpoint"
    
    # Attempt to delete the nonexistent endpoint
    result = delete_azure_model(random_endpoint_name)
    
    # For a nonexistent endpoint, the function should return False
    assert result is False, "Deletion of nonexistent endpoint should return False"