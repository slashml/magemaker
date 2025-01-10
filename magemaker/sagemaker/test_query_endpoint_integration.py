import pytest
import boto3
from magemaker.sagemaker.create_model import deploy_huggingface_model_to_sagemaker
from magemaker.sagemaker.query_endpoint import query_hugging_face_endpoint
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource
from magemaker.schemas.query import Query
from magemaker.session import session

@pytest.fixture(scope="module")
def sagemaker_client():
    """Create a SageMaker client for testing."""
    return boto3.client('sagemaker', region_name=session.region_name)

@pytest.fixture(scope="module")
def test_endpoint(sagemaker_client):
    """Create a test endpoint for querying."""
    model = Model(
        id="distilbert-base-uncased-finetuned-sst-2-english",
        source=ModelSource.HuggingFace
    )
    
    deployment = Deployment(
        destination="aws",
        instance_type="ml.t2.medium",
        instance_count=1
    )
    
    try:
        predictor = deploy_huggingface_model_to_sagemaker(deployment, model)
        
        waiter = sagemaker_client.get_waiter('endpoint_in_service')
        waiter.wait(
            EndpointName=predictor.endpoint_name,
            WaiterConfig={'Delay': 30, 'MaxAttempts': 20}
        )
        
        yield deployment, model, predictor.endpoint_name
        
        # Cleanup
        sagemaker_client.delete_endpoint(EndpointName=predictor.endpoint_name)
        print(f"Cleaned up endpoint: {predictor.endpoint_name}")
        
    except Exception as e:
        print(f"Error in setup: {str(e)}")
        if 'predictor' in locals() and hasattr(predictor, 'endpoint_name'):
            try:
                sagemaker_client.delete_endpoint(EndpointName=predictor.endpoint_name)
            except:
                pass
        raise

@pytest.mark.integration
def test_simple_sentiment_query(test_endpoint):
    """Test a simple positive sentiment query."""
    deployment, model, endpoint_name = test_endpoint
    
    # Test with a simple positive review
    query = Query(query="This is a great product, I really love it!")
    
    result = query_hugging_face_endpoint(endpoint_name, query, (deployment, model))
    
    # Verify the result format
    assert isinstance(result, list)
    assert len(result) == 1  # The result should be a list with one dictionary
    assert 'label' in result[0]
    assert 'score' in result[0]
    assert result[0]['label'] in ['POSITIVE', 'NEGATIVE']
    assert isinstance(result[0]['score'], float)
    assert 0 <= result[0]['score'] <= 1
    
    # For this positive text, expect POSITIVE label with high confidence
    assert result[0]['label'] == 'POSITIVE'
    assert result[0]['score'] > 0.9