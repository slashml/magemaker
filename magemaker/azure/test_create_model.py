
from magemaker.schemas.model import Model
from magemaker.schemas.deployment import Deployment

from magemaker.azure.create_model import deploy_huggingface_model_to_azure


def test_deploy_huggingface_model_to_azure():

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

    deploy_huggingface_model_to_azure(deployment=deployment, model=model)
    pass
