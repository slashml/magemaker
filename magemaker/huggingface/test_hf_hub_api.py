import pytest
from unittest.mock import patch, MagicMock
from magemaker.schemas.model import Model
from magemaker.huggingface.hf_hub_api import get_hf_task

@pytest.mark.unit
def test_get_hf_task_successful():
    with patch('magemaker.huggingface.hf_hub_api.hf_api') as mock_hf_api:
        mock_model_info = MagicMock()
        mock_model_info.pipeline_tag = "text-classification"
        mock_model_info.transformers_info = None
        mock_hf_api.model_info.return_value = mock_model_info

        model = Model(id="test-model", source="huggingface")
        task = get_hf_task(model)
        
        assert task == "text-classification"

@pytest.mark.unit
def test_get_hf_task_with_transformers_info():
    with patch('magemaker.huggingface.hf_hub_api.hf_api') as mock_hf_api:
        mock_model_info = MagicMock()
        mock_model_info.pipeline_tag = "old-task"
        mock_model_info.transformers_info = MagicMock(pipeline_tag="text-classification")
        mock_hf_api.model_info.return_value = mock_model_info

        model = Model(id="test-model", source="huggingface")
        task = get_hf_task(model)
        
        assert task == "text-classification"

@pytest.mark.unit
def test_get_hf_task_exception():
    with patch('magemaker.huggingface.hf_hub_api.hf_api') as mock_hf_api, \
         patch('magemaker.huggingface.hf_hub_api.console') as mock_console, \
         patch('magemaker.huggingface.hf_hub_api.print_error') as mock_print_error:
        
        mock_hf_api.model_info.side_effect = Exception("API error")

        model = Model(id="test-model", source="huggingface")
        task = get_hf_task(model)
        
        assert task is None
        mock_console.print_exception.assert_called_once()
        mock_print_error.assert_called_once()