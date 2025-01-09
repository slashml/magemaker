import pytest
from unittest.mock import patch, MagicMock
import sys

# Mock required modules before importing
sys.modules['datasets'] = MagicMock()
sys.modules['transformers'] = MagicMock()

from magemaker.schemas.training import Training
from magemaker.schemas.model import Model, ModelSource
from magemaker.sagemaker.fine_tune_model import fine_tune_model

@pytest.fixture
def sample_sagemaker_training():
    return Training(
        destination="aws",
        instance_type="ml.m5.xlarge",
        instance_count=1,
        output_path="s3://test-bucket/output",
        training_input_path="s3://test-bucket/train"
    )

@pytest.fixture
def sample_sagemaker_model():
    return Model(
        id="jumpstart-dft-bert-base-uncased-text-classification",
        source=ModelSource.Sagemaker,
        version="1.0"
    )

@patch('magemaker.sagemaker.fine_tune_model.sagemaker.hyperparameters.retrieve_default')
@patch('magemaker.sagemaker.fine_tune_model.train_model')
@patch('magemaker.sagemaker.fine_tune_model.JumpStartEstimator')
def test_fine_tune_sagemaker_model(
    mock_jumpstart_estimator, 
    mock_train_model, 
    mock_retrieve_default,
    sample_sagemaker_training, 
    sample_sagemaker_model
):
    # Mock hyperparameters retrieval
    mock_retrieve_default.return_value = {"param1": "value1"}

    # Setup mock estimator
    mock_estimator = MagicMock()
    mock_jumpstart_estimator.return_value = mock_estimator

    # Call fine_tune_model
    fine_tune_model(sample_sagemaker_training, sample_sagemaker_model)

    # Verify method calls
    mock_retrieve_default.assert_called_once()
    mock_jumpstart_estimator.assert_called_once()
    mock_train_model.assert_called_once()

@patch('magemaker.sagemaker.fine_tune_model.train_model')
def test_fine_tune_unsupported_model_sources(mock_train_model):
    # Test HuggingFace model source
    huggingface_model = Model(
        id="google-bert/bert-base-uncased",
        source=ModelSource.HuggingFace
    )
    training = Training(
        destination="aws",
        instance_type="ml.m5.xlarge",
        instance_count=1,
        training_input_path="s3://test-bucket/train"
    )

    with pytest.raises(NotImplementedError):
        fine_tune_model(training, huggingface_model)

    # Test Custom model source
    custom_model = Model(
        id="custom-model",
        source=ModelSource.Custom
    )

    with pytest.raises(NotImplementedError):
        fine_tune_model(training, custom_model)