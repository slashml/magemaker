from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.core.exceptions import ResourceNotFoundError

from dotenv import dotenv_values


def delete_azure_model(endpoint_name):
    # Initialize the ML client
    subscription_id   = dotenv_values(".env").get("AZURE_SUBSCRIPTION_ID")
    resource_group    = dotenv_values(".env").get("AZURE_RESOURCE_GROUP")
    workspace_name    = dotenv_values(".env").get("AZURE_WORKSPACE_NAME")

    try:
        credential = DefaultAzureCredential()
        ml_client = MLClient(
            credential=credential,
            subscription_id=subscription_id,
            resource_group_name=resource_group,
            workspace_name=workspace_name
        )
        
        # Check if endpoint exists
        try:
            endpoint = ml_client.online_endpoints.get(name=endpoint_name)
            print(f"Found endpoint: {endpoint_name}")
            
            # Delete the endpoint
            print(f"Deleting endpoint {endpoint_name}...")
            ml_client.online_endpoints.begin_delete(name=endpoint_name).wait()
            print(f"Successfully deleted endpoint: {endpoint_name}")
            return True
            
        except ResourceNotFoundError:
            print(f"Endpoint {endpoint_name} not found")
            return False
            
    except Exception as e:
        print(f"Error during endpoint deletion: {str(e)}")
        return False