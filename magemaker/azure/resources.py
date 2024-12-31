from typing import List
from google.cloud import aiplatform
from dotenv import dotenv_values

from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient



def list_azure_endpoints():
    """
    List all endpoints in an Azure ML workspace with their details
    
    Args:
        subscription_id (str): Azure subscription ID
        resource_group (str): Azure resource group name
        workspace_name (str): Azure ML workspace name
    """
    subscription_id   = dotenv_values(".env").get("AZURE_SUBSCRIPTION_ID")
    resource_group    = dotenv_values(".env").get("AZURE_RESOURCE_GROUP")
    workspace_name    = dotenv_values(".env").get("AZURE_WORKSPACE_NAME")

    print(subscription_id, resource_group, workspace_name)

    import logging
    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)

    # Initialize the ML client
    credential = DefaultAzureCredential()
    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name
    )
    
    try:
        # Get all endpoints
        endpoints = ml_client.online_endpoints.list()
        
        # Prepare data for tabulation
        endpoint_details = []
        
        for endpoint in endpoints:
            # Get deployments for this endpoint
            deployments = ml_client.online_deployments.list(endpoint_name=endpoint.name)
            deployment_details = []
            
            instance_type = None
            for deployment in deployments:
                if deployment.instance_count > 0:
                    deployment_details.append({
                        'model': deployment.model,
                        'InstanceType': deployment.instance_type,
                        'instance_count': deployment.instance_count
                    })
                    instance_type = deployment.instance_type
            
                # Get endpoint status
                endpoint_status = ml_client.online_endpoints.get(endpoint.name)
                
                endpoint_details.append({
                    'EndpointName': endpoint.name,
                    'status': endpoint_status.provisioning_state,
                    'scoring_uri': endpoint_status.scoring_uri,
                    'InstanceType': instance_type,
                    "__Provider": "AzureML",
                })
        
        # Print summary
        return endpoint_details
        
    except Exception as e:
        print(f"Error listing endpoints: {str(e)}")
        return None
