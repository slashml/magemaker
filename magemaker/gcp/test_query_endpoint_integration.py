import pytest
import os
from dotenv import load_dotenv
from magemaker.gcp.query_endpoint import query_vertexai_endpoint_rest

# Load environment variables
load_dotenv()
PROJECT_ID = os.getenv('PROJECT_ID')
GCLOUD_REGION = os.getenv('GCLOUD_REGION')

@pytest.fixture(scope="session", autouse=True)
def check_environment():
    """Check if environment is properly configured."""
    if not all([PROJECT_ID, GCLOUD_REGION]):
        pytest.skip("Required environment variables not set")

@pytest.mark.integration
def test_endpoint_query():
    """Test querying an actual endpoint."""
    try:
        # Use your actual endpoint ID here
        endpoint_id = "your-test-endpoint-id"
        test_input = "This is a test query."
        
        print(f"\nQuerying endpoint...")
        print(f"Project: {PROJECT_ID}")
        print(f"Region: {GCLOUD_REGION}")
        print(f"Input text: {test_input}")
        
        # Make the actual query
        response = query_vertexai_endpoint_rest(
            endpoint_id=endpoint_id,
            input_text=test_input
        )
        
        # Verify response structure
        assert isinstance(response, dict)
        print(f"\nResponse received: {response}")
        
    except Exception as e:
        print(f"\nQuery failed with error: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify endpoint ID is correct")
        print("2. Check GCP credentials")
        print("3. Verify endpoint is active")
        raise