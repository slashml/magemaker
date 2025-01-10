import pytest
import boto3
import json
import os
from magemaker.schemas.training import Training
from magemaker.schemas.model import Model, ModelSource
from magemaker.session import session, sagemaker_session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SAGEMAKER_ROLE = os.getenv('SAGEMAKER_ROLE')

@pytest.fixture(scope="module")
def sagemaker_client():
    """Create a SageMaker client for testing."""
    return boto3.client('sagemaker', region_name=session.region_name)

@pytest.fixture(scope="function")
def test_data():
    """Create and cleanup test data."""
    s3_client = boto3.client('s3')
    bucket = sagemaker_session.default_bucket()
    key = "test-data/train.jsonl"
    
    # Create simple training data
    training_data = [
        {"text": "great product", "label": 1},
        {"text": "bad quality", "label": 0},
        {"text": "excellent service", "label": 1},
        {"text": "terrible experience", "label": 0}
    ]
    
    # Convert to JSONL format
    jsonl_data = "\n".join(json.dumps(item) for item in training_data)
    
    # Upload to S3
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=jsonl_data.encode('utf-8')
    )
    
    training_path = f"s3://{bucket}/{key}"
    yield training_path, bucket
    
    # Cleanup
    try:
        s3_client.delete_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(f"Error cleaning up test data: {str(e)}")

@pytest.mark.integration
def test_training_setup(sagemaker_client, test_data):
    """Test training data setup and configuration."""
    if not SAGEMAKER_ROLE:
        pytest.skip("SAGEMAKER_ROLE environment variable not set")
    
    training_path, bucket = test_data
    try:
        # Verify S3 bucket exists
        s3_client = boto3.client('s3')
        response = s3_client.head_bucket(Bucket=bucket)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200
        print(f"✓ S3 bucket {bucket} exists and is accessible")
        
        # Verify training data exists
        obj = s3_client.get_object(Bucket=bucket, Key="test-data/train.jsonl")
        content = obj['Body'].read().decode('utf-8')
        data = [json.loads(line) for line in content.splitlines()]
        assert len(data) == 4
        assert all('text' in item and 'label' in item for item in data)
        print("✓ Training data is properly formatted")
        
        # Verify IAM role
        iam = boto3.client('iam')
        role_name = SAGEMAKER_ROLE.split('/')[-1]
        role = iam.get_role(RoleName=role_name)
        assert role['Role']['Arn'] == SAGEMAKER_ROLE
        print("✓ IAM role exists and is accessible")
        
        # Get available instance types
        instance_types = sagemaker_client.list_training_jobs(
            StatusEquals='Completed',
            MaxResults=10
        )
        print(f"Available completed training jobs: {len(instance_types.get('TrainingJobSummaries', []))}")
        
        # Success message
        print("\nSetup Verification Complete:")
        print(f"- Training data path: {training_path}")
        print(f"- IAM Role: {SAGEMAKER_ROLE}")
        print(f"- Region: {session.region_name}")
        
    except Exception as e:
        pytest.fail(f"Setup verification failed: {str(e)}")
        
    print("\nAll setup verifications passed successfully!")