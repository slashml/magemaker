import pytest
from magemaker.azure.create_model import deploy_huggingface_model_to_azure
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource
from dotenv import load_dotenv
import os

@pytest.mark.integration
def test_deploy_huggingface_model():
    """
    Integration test that uses actual deploy_huggingface_model_to_azure function
    with minimal compute requirements.
    """
    load_dotenv()
    
    model = Model(
        id="distilbert-base-uncased",
        source=ModelSource.HuggingFace
    )
    
    deployment = Deployment(
        destination="azure",
        instance_type="Standard_F2s_v2",
        instance_count=1,
        min_replica_count=1,
        max_replica_count=1
    )
    
    try:
        print("\nStarting minimal deployment test...")
        print(f"Model ID: {model.id}")
        print(f"Instance Type: {deployment.instance_type}")
        print(f"Replicas: {deployment.instance_count}")
        
        # Deploy model
        endpoint = deploy_huggingface_model_to_azure(deployment, model)
        
        # Verify deployment success
        if hasattr(endpoint, 'scoring_uri'):
            print(f"\nDeployment successful!")
            print(f"Endpoint URI: {endpoint.scoring_uri}")
            assert endpoint.scoring_uri.startswith('https://'), "Invalid endpoint URI"
            assert 'inference.ml.azure.com' in endpoint.scoring_uri, "Invalid Azure ML endpoint"
        else:
            # If scoring_uri not available, check other endpoint properties
            print(f"\nEndpoint created successfully")
            print(f"Endpoint details: {endpoint}")
            assert endpoint is not None, "Endpoint creation failed"
        
    except Exception as e:
        print(f"\nDeployment error: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Check Azure subscription quota")
        print("2. Verify resource group access")
        print("3. Check network connectivity")
        raise
    finally:
        # Add cleanup if needed
        print("\nTest completed - check Azure portal for endpoint status")