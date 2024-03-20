import boto3
import inquirer
import sagemaker
from enum import StrEnum, auto
from sagemaker.jumpstart.notebook_utils import list_jumpstart_models
from src.utils.rich_utils import print_error


class Frameworks(StrEnum):
    huggingface = auto()
    meta = auto()
    model = auto()
    tensorflow = auto()
    pytorch = auto()
    # autogluon
    # catboost
    # lightgbm
    mxnet = auto()
    # sklearn
    # xgboost


def search_sagemaker_jumpstart_model():
    """TODO: Pass region"""
    session = boto3.session.Session()
    sagemaker_session = sagemaker.session.Session(boto_session=session)

    questions = [
        inquirer.List('framework',
                      message="Which framework would you like to use?",
                      choices=[framework.value for framework in Frameworks]
                      ),
        inquirer.Text(
            'filter', message="Enter some text to search for a SageMaker model (e.g. ‘bert’)")
    ]
    answers = inquirer.prompt(questions)
    if answers is None:
        return
    model_filter = answers["filter"] or None
    filter_value = "framework == {}".format(answers["framework"])

    models = list_jumpstart_models(filter=filter_value,
                                   region='us-east-1', sagemaker_session=sagemaker_session)

    if model_filter is not None:
        models = list(filter(lambda x: model_filter in x, models))

    if len(models) == 0:
        print_error("No models found. Please try another")
    return models
