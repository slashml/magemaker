
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.mgmt.resource import ResourceManagementClient

from dotenv import dotenv_values
import os


def query_azure_endpoint(endpoint_name, query):
    # Initialize the ML client
    subscription_id   = dotenv_values(".env").get("AZURE_SUBSCRIPTION_ID")
    resource_group    = dotenv_values(".env").get("AZURE_RESOURCE_GROUP")
    workspace_name    = dotenv_values(".env").get("AZURE_WORKSPACE_NAME")

    credential = DefaultAzureCredential()
    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name
    )

    import json

    # Test data
    test_data = {
        "inputs": query
    }

    # Save the test data to a temporary file
    with open("test_request.json", "w") as f:
        json.dump(test_data, f)

    # Get prediction
    response = ml_client.online_endpoints.invoke(
        endpoint_name=endpoint_name,
        request_file = 'test_request.json'
    )

    print('Raw Response Content:', response)
    # delete a file
    os.remove("test_request.json")
    return response
