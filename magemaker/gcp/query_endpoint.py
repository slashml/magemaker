
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import json
from dotenv import dotenv_values


def query_vertexai_endpoint_rest(
    endpoint_id: str,
    input_text: str,
    token_path: str = None
):
    import google.auth
    import google.auth.transport.requests
    import requests

    # TODO: this will have to come from config files
    project_id = dotenv_values('.env').get('PROJECT_ID')
    location = dotenv_values('.env').get('GCLOUD_REGION')

    
    # Get credentials
    if token_path:
        credentials, project = google.auth.load_credentials_from_file(token_path)
    else:
        credentials, project = google.auth.default()
    
    # Refresh token
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    
    # Prepare headers and URL
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }
    
    url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/endpoints/{endpoint_id}:predict"
    
    # Prepare payload
    payload = {
        "instances": [
            {
                "inputs": input_text,
                # TODO: this also needs to come from configs
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.7,
                    "top_p": 0.95
                }
            }
        ]
    }
    
    # Make request
    response = requests.post(url, headers=headers, json=payload)
    print('Raw Response Content:', response.content.decode())

    return response.json()
