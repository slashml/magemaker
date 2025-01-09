import click
import yaml
from rich.console import Console
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model
from magemaker.sagemaker.create_model import deploy_huggingface_model_to_sagemaker
from magemaker.gcp.create_model import deploy_huggingface_model_to_vertexai

console = Console()

@click.group()
def main():
    """Magemaker CLI for model deployment"""
    pass

@main.command()
@click.option('--deploy', type=click.Path(exists=True), help='Path to deployment YAML file')
def deploy(deploy):
    """Deploy a model using configuration from YAML file"""
    with open(deploy, 'r') as f:
        config = yaml.safe_load(f)
    
    deployment = Deployment(**config['deployment'])
    model = Model(**config['model'])
    
    if deployment.destination == "sagemaker":
        deploy_huggingface_model_to_sagemaker(deployment, model)
    elif deployment.destination == "gcp":
        deploy_huggingface_model_to_vertexai(deployment, model)
    
if __name__ == '__main__':
    main()