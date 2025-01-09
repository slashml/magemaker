import pytest
from unittest.mock import patch, MagicMock
import sys

sys.modules['inquirer'] = MagicMock()
sys.modules['InquirerPy'] = MagicMock()

from magemaker.schemas.query import Query
from magemaker.sagemaker.query_endpoint import make_query_request
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model

def test_make_query_request():
    with patch('magemaker.sagemaker.query_endpoint.is_sagemaker_model') as mock_is_sagemaker, \
         patch('magemaker.sagemaker.query_endpoint.query_sagemaker_endpoint') as mock_sagemaker_query, \
         patch('magemaker.sagemaker.query_endpoint.query_hugging_face_endpoint') as mock_hf_query:
        
        # Test Sagemaker model
        mock_is_sagemaker.return_value = True
        mock_sagemaker_query.return_value = "Sagemaker result"
        
        query = Query(query="Test query")
        config = (MagicMock(), MagicMock())
        
        result = make_query_request("test-endpoint", query, config)
        assert result == "Sagemaker result"

        # Test HuggingFace model
        mock_is_sagemaker.return_value = False
        mock_hf_query.return_value = "HuggingFace result"
        
        result = make_query_request("test-endpoint", query, config)
        assert result == "HuggingFace result"