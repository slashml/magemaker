from typing import List
from google.cloud import aiplatform
from dotenv import dotenv_values


def list_vertex_ai_endpoints(filter_str: str = None) -> List[str]:
    # Initialize Vertex AI

    project_id = dotenv_values('.env').get('PROJECT_ID')
    location = dotenv_values('.env').get('GCLOUD_REGION')

    # project_id = "omega-vigil-421204"  # Replace with your project ID
    # location = "us-central1"
    aiplatform.init(project=project_id, location=location)

    # Get endpoint client
    endpoints_client = aiplatform.Endpoint.list(
        project=project_id,
        location=location
    )
    
    # Extract relevant information from each endpoint
    endpoint_details = []
    for endpoint in endpoints_client:
        details = {
            'EndpointName': endpoint.display_name,
            # this is a unified name in the entire magemaker system
            # this needs to be paramterized
            'resource_name': endpoint.resource_name,
            'deployed_models': [],
            'InstanceType': None,
            '__Provider': 'VertexAI'
        }
        
        # Get information about deployed models
        for deployed_model in endpoint.gca_resource.deployed_models:
            model_info = {
                'model_id': deployed_model.model,
                'InstanceType': deployed_model.dedicated_resources.machine_spec.machine_type
                if hasattr(deployed_model, 'dedicated_resources') else None
            }
            details['deployed_models'].append(model_info)
            
            # Get the machine type from the first deployed model
            if details['InstanceType'] is None and model_info['InstanceType']:
                details['InstanceType'] = model_info['InstanceType']
        
        endpoint_details.append(details)

    return endpoint_details