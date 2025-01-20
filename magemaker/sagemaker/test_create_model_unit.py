import pytest
import tempfile
import os
from unittest.mock import MagicMock, patch
from magemaker.sagemaker.create_model import (
    deploy_huggingface_model_to_sagemaker,
    deploy_custom_huggingface_model,
    create_and_deploy_jumpstart_model
)
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource

@pytest.fixture
def sample_deployment():
    return Deployment(destination="aws", instance_type="ml.m5.xlarge", instance_count=1)

@pytest.mark.unit
@patch('magemaker.sagemaker.create_model.S3Uploader.upload')
@patch('magemaker.sagemaker.create_model.HuggingFaceModel')
@patch('magemaker.sagemaker.create_model.sagemaker_session')
def test_custom_model_deployment(sagemaker_session, mock_hf_model, mock_s3_upload, sample_deployment, tmp_path):
    # Create a mock model file
    test_model_file = tmp_path / "model.pt"
    test_model_file.write_text("dummy model content")

    # Mock S3 upload and model deployment
    mock_s3_upload.return_value = "s3://test-bucket/models/test-custom-model"

    mock_predictor = MagicMock()
    mock_predictor.endpoint_name = "test-endpoint-001"

    mock_hf_model_return = mock_hf_model.return_value
    mock_hf_model_return.deploy.return_value = mock_predictor


    sagemaker_session.default_bucket.return_value = "test-bucket"

    custom_model = Model(
        id="test-custom-model",
        source=ModelSource.Custom,
        location=str(test_model_file)
    )

    predictor = deploy_custom_huggingface_model(sample_deployment, custom_model)
    
    assert predictor.endpoint_name == "test-endpoint-001"
    mock_s3_upload.assert_called_once()
    mock_hf_model_return.deploy.assert_called_once()

@pytest.mark.unit
@patch('magemaker.sagemaker.create_model.JumpStartModel')
def test_jumpstart_model_deployment(mock_jumpstart_model, sample_deployment):
    # Use a valid JumpStart model ID
    jumpstart_model = Model(
        id="jumpstart-dft-bert-base-uncased-text-classification", 
        source=ModelSource.Sagemaker
    )
    
    # Mock the JumpStart model deployment
    mock_predictor = MagicMock()
    mock_predictor.endpoint_name = "test-jumpstart-endpoint"
    mock_jumpstart_model_return = mock_jumpstart_model.return_value
    mock_jumpstart_model_return.deploy.return_value = mock_predictor

    predictor = create_and_deploy_jumpstart_model(sample_deployment, jumpstart_model)
    
    assert predictor.endpoint_name == "test-jumpstart-endpoint"
    mock_jumpstart_model.assert_called_once()