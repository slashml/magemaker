import os
import pytest

from magemaker.azure.query_endpoint import query_azure_endpoint

def test_query_nonexistent_endpoint():
    """
    Test querying a nonexistent endpoint
    """
    # Ensure we have the required environment variables
    required_vars = ['AZURE_SUBSCRIPTION_ID', 'AZURE_RESOURCE_GROUP', 'AZURE_WORKSPACE_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        pytest.skip(f"Missing environment variables: {missing_vars}")
    
    # Use a fictitious endpoint name
    nonexistent_endpoint_name = "test-nonexistent-endpoint"
    
    # Prepare a sample query
    sample_query = {
        "text": "This is a test query"
    }
    
    # Expect an exception when querying a nonexistent endpoint
    with pytest.raises(Exception):
        query_azure_endpoint(nonexistent_endpoint_name, sample_query)



# def test_query_endpoint_rest():

#     endpoint_id = '1234567890'
#     input_text = 'This is a test'

#     resp = query_azure_endpoint(endpoint_id=endpoint_id, input_text=input_text)
