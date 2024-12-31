from typing import List
from google.cloud import aiplatform

from magemaker.console import console
from rich.table import Table
from magemaker.schemas.model import Model
from magemaker.schemas.deployment import Deployment
from dotenv import dotenv_values
from magemaker.utils.model_utils import get_unique_endpoint_name


from magemaker.config import write_config

HUGGING_FACE_HUB_TOKEN = dotenv_values(".env").get("HUGGING_FACE_HUB_KEY")

def deploy_huggingface_model_to_vertexai(deployment:Deployment, model: Model):
    location = dotenv_values(".env").get("GCLOUD_REGION")
    project_id = dotenv_values(".env").get("PROJECT_ID")

    _deploy_model(project_id=project_id, location=location, model=model, deployment=deployment)
    pass

def _deploy_model(
    *,
    project_id: str = None,
    location: str = None,
    model: Model = None,
    deployment: Deployment = None
):
    """
    Deploy a Hugging Face model using pre-built container
    """

    aiplatform.init(project=project_id, location=location)

    env_vars = {
        "MODEL_ID": model.id,
        "MAX_INPUT_LENGTH": "512",
        "MAX_TOTAL_TOKENS": "1024",
        "MAX_BATCH_PREFILL_TOKENS": "2048",
        "NUM_SHARD": "1",
        # "HF_TOKEN": ""  # Add your Hugging Face token if needed
    }

    if HUGGING_FACE_HUB_TOKEN is not None: 
        env_vars['HF_TOKEN'] = HUGGING_FACE_HUB_TOKEN

    display_name = get_unique_endpoint_name(
        model.id, deployment.endpoint_name)

    # Create model using pre-built container
    model_artifact = aiplatform.Model.upload(
        display_name=display_name,
        serving_container_image_uri="us-docker.pkg.dev/deeplearning-platform-release/gcr.io/huggingface-text-generation-inference-cu121.2-2.ubuntu2204.py310",
        serving_container_environment_variables=env_vars
    )

    console.log(
        "Deploying model to GCP. [magenta]This may take up to 10 minutes for very large models.[/magenta]")

    # console.print(f"https://console.cloud.google.com/vertex-ai/models/locations/{location}/models/{model.id}/versions/1/deploy?project={project_id}")

    with console.status("[bold green]Deploying model...") as status:
        table = Table(show_header=False, header_style="magenta")
        table.add_column("Resource", style="dim")
        table.add_column("Value", style="blue")
        # table.add_row("model", model)
        table.add_row("GCP instance type", deployment.instance_type)
        table.add_row("Number of instances", str(
            deployment.instance_count))

        console.print(table)

        try:
            print(f"model uploaded: {model_artifact.resource_name}")

            # Deploy the model
            endpoint = model_artifact.deploy(
                machine_type=deployment.instance_type,
                accelerator_type=deployment.accelerator_type if deployment.accelerator_type else None,
                accelerator_count=deployment.accelerator_count if deployment.accelerator_count else 0,
                min_replica_count=deployment.min_replica_count if deployment.min_replica_count else 1,
                max_replica_count=deployment.max_replica_count if deployment.max_replica_count else 1,
                sync=True
            )
            
            print(f"Model deployed to endpoint: {endpoint.resource_name}")
            return endpoint

        except:
            console.log("[magenta]An error occurred[/magenta]")
            console.print_exception()
            quit()

    print_success(
        f"{model.id} is now up and running at the endpoint [blue]{predictor.endpoint_name}")

    write_config(deployment, model)
    return predictor