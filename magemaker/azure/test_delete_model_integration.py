import pytest
from magemaker.azure.delete_model import delete_azure_model
from dotenv import load_dotenv
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import os

@pytest.mark.integration
def test_delete_model():
    """
    Integration test for deleting the model that was deployed in create_model test.
    Uses the same model ID pattern as create test.
    """
    load_dotenv()
    
    try:
        # Get Azure ML client to list endpoints
        credential = DefaultAzureCredential()
        ml_client = MLClient(
            credential=credential,
            subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
            resource_group_name=os.getenv('AZURE_RESOURCE_GROUP'),
            workspace_name=os.getenv('AZURE_WORKSPACE_NAME')
        )
        
        # List endpoints that match our model pattern
        endpoints = ml_client.online_endpoints.list()
        endpoint_to_delete = None
        
        # Find endpoint created by the create test (starts with hf-ep-)
        for endpoint in endpoints:
            if endpoint.name.startswith('hf-ep-'):
                endpoint_to_delete = endpoint.name
                break
        
        if not endpoint_to_delete:
            pytest.skip("No endpoint found from create test")
            
        print(f"\nFound endpoint to delete: {endpoint_to_delete}")
        
        # Test deletion
        result = delete_azure_model(endpoint_to_delete)
        
        # Verify deletion
        assert result is True, f"Failed to delete endpoint: {endpoint_to_delete}"
        print(f"✓ Successfully deleted endpoint: {endpoint_to_delete}")
        
    except Exception as e:
        print(f"\nDeletion failed: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify create test has run successfully")
        print("2. Check endpoint exists in Azure ML workspace")
        print("3. Verify Azure permissions")
        raise


def test_deploy_huggingface_model_to_azure():

    deployment = Deployment(
        endpoint_name="test-endpoint",
        instance_type="Standard_DS3_v2",
        destination="azure",
        instance_count=1,
        quantization=None,
        num_gpus=None
    )

    model = Model(
        id="facebook-opt-125m",
        source="huggingface",
    )

    deploy_huggingface_model_to_azure(deployment=deployment, model=model)
    pass