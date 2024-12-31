from typing import List
from google.cloud import aiplatform

from dotenv import dotenv_values

# delete a model from vertex ai
def delete_vertex_ai_model(
    endpoint_id: str,
):
    project_id = dotenv_values('.env').get('PROJECT_ID')
    location = dotenv_values('.env').get('GCLOUD_REGION')
    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # Get the endpoint
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_id)
    
    # If no specific model_id provided, get all deployed models
    deployed_models = endpoint.list_models()
    print(f"Found {len(deployed_models)} deployed models")
    
    # Undeploy all models from the endpoint
    for deployed_model in deployed_models:
        print(f"Undeploying model: {deployed_model.id}")
        endpoint.undeploy(deployed_model.id)
        
        # Get the model resource and delete it
        try:
            model = aiplatform.Model(model_name=deployed_model.id)
            print(f"Deleting model: {deployed_model.id}")
            model.delete()
        except Exception as e:
            print(f"Error deleting model {deployed_model.id}: {str(e)}")

    
    # Delete the endpoint
    print(f"Deleting endpoint: {endpoint_id}")
    endpoint.delete()
    
    print("Deletion process completed successfully")
