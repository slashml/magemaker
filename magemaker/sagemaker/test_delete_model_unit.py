import pytest
from unittest.mock import patch, MagicMock
from magemaker.sagemaker.delete_model import delete_sagemaker_model

@pytest.mark.unit
def test_delete_sagemaker_model():
    # Test deleting multiple endpoints
    with patch('boto3.client') as mock_boto_client:
        mock_sagemaker_client = MagicMock()
        mock_boto_client.return_value = mock_sagemaker_client

        endpoints = ['endpoint1', 'endpoint2']
        delete_sagemaker_model(endpoints)

        # Check that delete_endpoint was called for each endpoint
        assert mock_sagemaker_client.delete_endpoint.call_count == 2
        mock_sagemaker_client.delete_endpoint.assert_any_call(EndpointName='endpoint1')
        mock_sagemaker_client.delete_endpoint.assert_any_call(EndpointName='endpoint2')

@pytest.mark.unit
def test_delete_empty_endpoints():
    # Test deleting with empty list
    with patch('magemaker.sagemaker.delete_model.print_success') as mock_print_success:
        delete_sagemaker_model([])
        mock_print_success.assert_called_once_with("No Endpoints to delete!")