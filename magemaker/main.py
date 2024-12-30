import inquirer
import logging
import threading
from InquirerPy import prompt
from magemaker.sagemaker import EC2Instance
from magemaker.sagemaker.create_model import deploy_model
from magemaker.sagemaker.delete_model import delete_sagemaker_model
from magemaker.sagemaker.resources import list_sagemaker_endpoints, select_instance, list_service_quotas_async
from magemaker.sagemaker.query_endpoint import make_query_request
from magemaker.sagemaker.search_jumpstart_models import search_sagemaker_jumpstart_model

from magemaker.gcp.resources import list_vertex_ai_endpoints
from magemaker.gcp.delete_model import delete_vertex_ai_model

from magemaker.utils.rich_utils import print_error, print_success
from magemaker.schemas.deployment import Deployment, Destination
from magemaker.schemas.model import Model, ModelSource
from magemaker.schemas.query import Query
from magemaker.config import get_config_for_endpoint
from enum import StrEnum
from rich import print


class Actions(StrEnum):
    LIST = "Show active model endpoints"
    DEPLOY = "Deploy a model endpoint"
    DELETE = "Delete a model endpoint"
    QUERY = "Query a model endpoint"
    EXIT = "Quit"
    # TRAIN = "fine tune a model"

import os

# set AWS_REGION in env
os.environ["AWS_REGION"] = "us-west-2"


def fetch_active_endpoints():
    sagemaker_endpoints = list_sagemaker_endpoints()
    vertex_ai_endpoints = list_vertex_ai_endpoints()

    return sagemaker_endpoints + vertex_ai_endpoints



def print_active_endpoints(active_endpoints):
    for endpoint in active_endpoints:
        endpoint_id = endpoint.get('resource_name','').split('/')[-1]
        endpoint_str = f'with id [green]{endpoint_id}[/green]' if endpoint_id else ''
        if endpoint.get("InstanceType"):
            print(f"[blue]{endpoint['EndpointName']}[/blue] running on an [green]{endpoint['InstanceType']} [/green] instance {endpoint_str}")
        else:
            print(f"[blue]{endpoint['EndpointName']}[/blue] running on an [red]Unknown[/red] instance")


def delete_endpoint(endpoint_name):
    print('Deleting endpoint...', endpoint_name)
    import pdb
    pdb.set_trace()

    for endpoint in endpoint_name:
        name, provider, resource_name = endpoint

        if provider == 'Sagemaker':
            delete_sagemaker_model([name])

        if provider == 'VertexAI':
            endpoint_id = resource_name.split('/')[-1] 
            delete_vertex_ai_model(endpoint_id)



def main(args=None, loglevel='INFO'):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    print("[magenta]Magemaker by SlashML")
    
    # list_service_quotas is a pretty slow API and it's paginated.
    # Use async here and store the result in instances
    instances = []
    instance_thread = threading.Thread(
        target=list_service_quotas_async, args=[instances])
    instance_thread.start()

    while True:
        active_endpoints = fetch_active_endpoints()
        questions = [
            inquirer.List(
                'action',
                message="What would you like to do?",
                choices=[e.value for e in Actions]
            )
        ]
        answers = inquirer.prompt(questions)
        if (answers is None):
            break

        action = answers['action']

        match action:
            case Actions.LIST:
                if len(active_endpoints) != 0:
                    sagemaker_endpoints = list_sagemaker_endpoints()
                    vertex_ai_endpoints = list_vertex_ai_endpoints()
                    # printing sagemaker endpoints
                    print("[green]Sagemaker[/green] Endpoints:")
                    print_active_endpoints(sagemaker_endpoints) 
                    print('\n')

                    print('[green]GCP[/green] Endpoints')
                    print_active_endpoints(vertex_ai_endpoints) 
                    print('\n')
                    print('\n')
                else:
                    print_error('No active endpoints.\n')
            case Actions.DEPLOY:
                build_and_deploy_model(instances, instance_thread)
            case Actions.DELETE:
                if (len(active_endpoints) == 0):
                    print_success("No Endpoints to delete!")
                    continue

                questions = [
                    inquirer.Checkbox('endpoints',
                                      message="Which endpoints would you like to delete? (space to select)",
                                      choices=[(endpoint['EndpointName']+'-'+endpoint.get('resource_name', '').split('/')[-1], (endpoint['EndpointName'], endpoint['__Provider'], endpoint.get('resource_name', '')))
                                               for endpoint in active_endpoints]
                                      )
                ]
                answers = inquirer.prompt(questions)
                if (answers is None):
                    continue

                endpoints_to_delete = answers['endpoints']
                delete_endpoint(endpoints_to_delete)
            case Actions.QUERY:
                if (len(active_endpoints) == 0):
                    print_success("No Endpoints to query!")
                    continue

                questions = [
                    {
                        "type": "list",
                        "message": "Which endpoint would you like to query?",
                        "name": 'endpoint',
                        "choices": [endpoint['EndpointName'] for endpoint in active_endpoints]
                    },
                    {
                        "type": "input",
                        "message": "What would you like to query?",
                        "name": 'query'
                    }
                ]
                answers = prompt(questions)
                if (answers is None):
                    continue

                endpoint = answers['endpoint']
                query = Query(query=answers['query'])
                config = get_config_for_endpoint(endpoint)

                # support multi-model endpoints
                if config:
                    config = (config.deployment, config.models[0])
                    make_query_request(endpoint, query, config)
                
                print('Config for this model not found, try another model')

            case Actions.EXIT:
                quit()

    print_success("Goodbye!")


class ModelType(StrEnum):
    SAGEMAKER = "Deploy a Sagemaker model"
    HUGGINGFACE = "Deploy a Hugging Face model"
    CUSTOM = "Deploy a custom model"


def build_and_deploy_model(instances, instance_thread):
    questions = [
        inquirer.List(
            'model_type',
            message="Choose a model type:",
            choices=[model_type.value for model_type in ModelType]
        )
    ]
    answers = inquirer.prompt(questions)
    if answers is None:
        return

    model_type = answers['model_type']

    match model_type:
        case ModelType.SAGEMAKER:
            models = []
            while len(models) == 0:
                models = search_sagemaker_jumpstart_model()
                if models is None:
                    quit()

            questions = [
                {
                    "type": "fuzzy",
                    "name": "model_id",
                    "message": "Choose a model. Search by task (e.g. eqa) or model name (e.g. llama):",
                    "choices": models,
                    "match_exact": True,
                }
            ]
            answers = prompt(questions)
            if (answers is None):
                return

            model_id, model_version = answers['model_id'], "2.*"
            instance_thread.join()
            instance_type = select_instance(instances)

            model = Model(
                id=model_id,
                model_version=model_version,
                source=ModelSource.Sagemaker
            )

            deployment = Deployment(
                instance_type=instance_type,
                destination=Destination.AWS,
                num_gpus=4 if instance_type == EC2Instance.LARGE else 1
            )

            predictor = deploy_model(deployment=deployment, model=model)
        case ModelType.HUGGINGFACE:
            questions = [
                inquirer.Text(
                    'model_id',
                    message="Enter the exact model name from huggingface.co (e.g. google-bert/bert-base-uncased)",
                )
            ]
            answers = inquirer.prompt(questions)
            if answers is None:
                return

            model_id = answers['model_id']
            instance_thread.join()
            instance_type = select_instance(instances)

            model = Model(
                id=model_id,
                source=ModelSource.HuggingFace
            )

            deployment = Deployment(
                instance_type=instance_type,
                destination=Destination.AWS,
            )

            predictor = deploy_model(deployment=deployment, model=model)

        case ModelType.CUSTOM:
            questions = [
                {
                    "type": "input",
                    "message": "What is the local path or S3 URI of the model?",
                    "name": "path"
                },
                {
                    "type": "input",
                    "message": "What is the base model that was fine tuned? (e.g. google-bert/bert-base-uncased)",
                    "name": "base_model"
                }
            ]
            answers = prompt(questions)
            local_path = answers['path']
            base_model = answers['base_model']

            instance_thread.join()
            instance_type = select_instance(instances)

            model = Model(
                id=base_model,
                source=ModelSource.Custom,
                location=local_path
            )

            deployment = Deployment(
                instance_type=instance_type,
                destination=Destination.AWS
            )
            deploy_model(deployment=deployment, model=model)
