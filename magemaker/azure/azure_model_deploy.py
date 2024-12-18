from azureml.core import Workspace, Environment, Model
from azureml.core.webservice import AciWebservice, Webservice
from azureml.core.model import InferenceConfig
from azureml.core.compute import AmlCompute
import os

def deploy_to_azure_ml(deployment, model):
    ws = Workspace.from_config() 

    compute_target = AmlCompute(ws, name=deployment.compute_target)

    env = Environment.from_conda_specification(name="myenv", file_path="environment.yml") 

    inference_config = InferenceConfig(entry_script="score.py", environment=env) 

    model = Model.register(workspace=ws, model_path=model.location, model_name=model.id)

    deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

    service = Model.deploy(
        ws,
        deployment.endpoint_name,  
        [model],  
        inference_config, 
        deployment_config, 
        compute_target=compute_target 
    )

    service.wait_for_deployment(show_output=True)

    print(f"Model deployed to Azure at endpoint: {service.scoring_uri}")
    return service
