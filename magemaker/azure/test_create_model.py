
from magemaker.schemas.model import Model
from magemaker.schemas.deployment import Deployment

from magemaker.gcp.create_model import deploy_huggingface_model_to_vertexai


def test_deploy_huggingface_model_to_vertexai():

    deployment = Deployment(
        endpoint_name="test-endpoint",
        instance_type="Standard_DS3_v2",
        destination="azure",
        instance_count=1,
        quantization=None,
        num_gpus=None
    )

    model = Model(
        id="facebook-opt-125m",
        source="huggingface",
    )

    deploy_huggingface_model_to_vertexai(deployment=deployment, model=model)
    pass
