from unittest.mock import patch, MagicMock
from magemaker.gcp.delete_model import delete_vertex_ai_model

@patch('google.cloud.aiplatform.Model')
@patch('google.cloud.aiplatform.Endpoint')
@patch('google.cloud.aiplatform.init')
def test_delete_vertex_ai_model(mock_init, mock_endpoint_class, mock_model_class):
    # Setup mocks
    mock_endpoint = MagicMock()
    mock_endpoint_class.return_value = mock_endpoint
    
    # Mock deployed models
    mock_model = MagicMock()
    mock_model.id = 'test_model_id'
    mock_endpoint.list_models.return_value = [mock_model]
    
    # Test deletion
    endpoint_id = 'test_endpoint_id'
    delete_vertex_ai_model(endpoint_id=endpoint_id)
    
    # Verify calls
    mock_endpoint.undeploy.assert_called_once_with('test_model_id')
    mock_model_class.assert_called_once_with(model_name='test_model_id')
    mock_model_class.return_value.delete.assert_called_once()
    mock_endpoint.delete.assert_called_once()