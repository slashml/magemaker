import inquirer
from enum import StrEnum, auto
from sagemaker.jumpstart.notebook_utils import list_jumpstart_models
from magemaker.utils.rich_utils import print_error
from magemaker.session import session, sagemaker_session


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
    questions = [
        inquirer.List('framework',
                      message="Which framework would you like to use?",
                      choices=[framework.value for framework in Frameworks]
                      ),
    ]
    answers = inquirer.prompt(questions)
    if answers is None:
        return
    filter_value = "framework == {}".format(answers["framework"])

    models = list_jumpstart_models(filter=filter_value,
                                   region=session.region_name, sagemaker_session=sagemaker_session)
    return models
