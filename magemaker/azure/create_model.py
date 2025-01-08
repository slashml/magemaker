
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.mgmt.resource import ResourceManagementClient

from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    AmlCompute
)

from magemaker.config import write_config

from magemaker.console import console
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

from dotenv import dotenv_values

# Deployment
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model

from magemaker.utils.model_utils import get_unique_endpoint_name
from magemaker.utils.rich_utils import print_error, print_success

HUGGING_FACE_HUB_TOKEN = dotenv_values(".env").get("HUGGING_FACE_HUB_KEY")

def deploy_huggingface_model_to_azure(deployment:Deployment, model: Model):
    subscription_id = dotenv_values(".env").get("AZURE_SUBSCRIPTION_ID")
    resource_group = dotenv_values(".env").get("AZURE_RESOURCE_GROUP")
    workspace_name = dotenv_values(".env").get("AZURE_WORKSPACE_NAME")

    _deploy_model(subscription_id, resource_group, workspace_name, deployment, model)
    pass


def _deploy_model(subscription_id, resource_group, workspace_name, deployment: Deployment, model:Model):

    credential = DefaultAzureCredential()

    ml_client = MLClient(
        credential = credential,
        subscription_id = subscription_id,
        resource_group_name = resource_group,
        workspace_name = workspace_name
    )

    try:
        workspace = ml_client.workspaces.get(name=workspace_name)
        print(f"Found workspace: {workspace.name}")
    except Exception as e:
        print(f"Error accessing workspace: {str(e)}")


    # Create a unique endpoint name
    registry_name = "HuggingFace" if model.source == "huggingface" else "Custom"
    model_id = f"azureml://registries/{registry_name}/models/{model.id}/labels/latest"

    import time
    endpoint_name="hf-ep-" + str(int(time.time())) # endpoint name must be unique per Azure region, hence appending timestamp 
    
    print('endpoint name', endpoint_name)

    print('Deploying model started, waiting for the endpoint to be up ...')

    # wait for the endpoint to be up
    ml_client.begin_create_or_update(ManagedOnlineEndpoint(name=endpoint_name)).wait()


    # Create environment for the deployment
    environment = Environment(
        name="bert-env",
        image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest",
        conda_file={
            "channels": ["conda-forge", "pytorch"],
            "dependencies": [
                "python=3.11",
                "pip",
                "pytorch",
                "transformers",
                "numpy"
            ]
        }
    )

    console.log(
        "Deploying model to Azure. [magenta]This may take up to 10 minutes for very large models.[/magenta]")

    # console.print(f"https://console.cloud.google.com/vertex-ai/models/locations/{location}/models/{model.id}/versions/1/deploy?project={project_id}")

    with console.status("[bold green]Deploying model...") as status:
        table = Table(show_header=False, header_style="magenta")
        table.add_column("Resource", style="dim")
        table.add_column("Value", style="blue")
        # table.add_row("model", model)
        table.add_row("Azure instance type", deployment.instance_type)
        table.add_row("Number of instances", str(
            deployment.instance_count))

        console.print(table)

        try:

            print('endpoint created', endpoint_name)

            ml_client.online_deployments.begin_create_or_update(ManagedOnlineDeployment(
                name="demo",
                endpoint_name=endpoint_name,
                model=model_id,
                environment=environment,
                instance_type=deployment.instance_type,
                instance_count=deployment.instance_count,
            )).wait()


            endpoint = ml_client.online_endpoints.get(endpoint_name)
            endpoint.traffic = {"demo": 100}
            ml_client.begin_create_or_update(endpoint).result()

            print(f"Model deployed to endpoint: {endpoint.scoring_uri}")
            return endpoint

        except:
            console.log("[magenta]An error occurred[/magenta]")
            console.print_exception()
            quit()

    print_success(
        f"{model.id} is now up and running at the endpoint [blue]{endpoint.scoring_uri}")

    write_config(deployment, model)
    return endpoint