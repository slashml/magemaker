import pytest
from unittest.mock import patch, MagicMock

# Assuming resources.py has a function named list_sagemaker_endpoints
from .resources import list_sagemaker_endpoints


@patch("boto3.client")
def test_list_sagemaker_endpoints_no_filter(mock_boto_client):
    mock_client_instance = MagicMock()
    mock_client_instance.list_endpoints.return_value = {
        "Endpoints": [
            {"EndpointName": "endpoint1"},
            {"EndpointName": "endpoint2"},
        ]
    }

    mock_boto_client.return_value = mock_client_instance

    endpoints = list_sagemaker_endpoints()
    assert len(endpoints) == 2
    assert endpoints[0]['EndpointName'] == 'endpoint1'
    assert endpoints[1]['EndpointName'] == 'endpoint2'


# def test_list_sagemaker_endpoints_no_filter():
#     # actual call for quick testing
#     endpoints = list_sagemaker_endpoints()