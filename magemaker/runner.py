import argparse
import logging
import sys
import traceback
import yaml
logging.getLogger("sagemaker.config").setLevel(logging.WARNING)
logging.getLogger("botocore.credentials").setLevel(logging.WARNING)
import os
from magemaker.sagemaker.create_model import deploy_huggingface_model_to_sagemaker, deploy_custom_huggingface_model
from magemaker.sagemaker.fine_tune_model import fine_tune_model
from magemaker.schemas.deployment import Deployment
from magemaker.schemas.model import Model, ModelSource
import subprocess
from magemaker.main import main, deploy_model

RED='\033[0;31m'  #red
NC='\033[0m' # No Color
YELLOW='\033[1;33m'
GREEN='\033[0;32m'



def runner():
    # if (not os.path.exists(os.path.expanduser('~/.aws')) or not os.path.exists('.env')):
    #     os.system("bash setup.sh")

    parser = argparse.ArgumentParser(
        description="Create, deploy, query against models.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')
    parser.add_argument(
        "--hf",
        help="Deploy a Hugging Face Model.",
        type=str
    )
    parser.add_argument(
        "--instance",
        help="EC2 instance type to deploy to.",
        type=str
    )
    parser.add_argument(
        "--deploy",
        help="path to YAML deployment configuration file",
        type=str
    )
    parser.add_argument(
        "--train",
        help="path to YAML training configuration file",
        type=str
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    
    parser.add_argument(
        "--cloud", 
        choices=['aws', 'gcp', 'azure', 'all'], 
        help="Specify the cloud provider for configuration and deployment"
    )
    if len(sys.argv) == 1:
        # just for the case of magemaker
        # parser.print_help()
        print(f"{RED}Error: You must specify a cloud provider.{NC}")
        print(f"{GREEN}Possible solutions:{NC}")
        print(f"{YELLOW}- magemaker --cloud gcp{NC}")
        print(f"{YELLOW}- magemaker --cloud aws{NC}")
        print(f"{YELLOW}- magemaker --cloud azure{NC}")
        print(f"{YELLOW}- magemaker --cloud all{NC}")
        sys.exit(1)

    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    preflight_path = os.path.join(script_dir, 'scripts', 'preflight.sh')
    cmd = ["bash", preflight_path]

    if args.cloud:
        if args.deploy is not None:
            print(f"{RED}Error: You cannot specify a deployment configuration file with the --cloud flag. We will pick the destination from the yaml file{NC}")
        else:
            cmd.extend(["--cloud", args.cloud])
            subprocess.run(cmd, check=True)

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    # if args.hf is not None:
    #     instance_type = args.instance or "ml.m5.xlarge"
    #     predictor = deploy_huggingface_model(args.hf, instance_type)
    #     quit()

    if args.deploy is not None:
        try:
            deployment = None
            model = None
            with open(args.deploy) as config:
                configuration = yaml.safe_load(config)
                deployment = configuration['deployment']

                # TODO: Support multi-model endpoints
                model = configuration['models'][0]

            destination = deployment.destination
            # Run the script
            print(f"Destination for deployment: {destination}")
            cmd.extend(["--cloud", destination])
            subprocess.run(cmd, check=True)

            deploy_model(deployment, model)
        except:
            traceback.print_exc()
            print("File not found")

        quit()

    if args.train is not None:
        try:
            train = None
            model = None
            with open(args.train) as config:
                configuration = yaml.safe_load(config)
                training = configuration['training']
                model = configuration['models'][0]
            fine_tune_model(training, model)
        except:
            traceback.print_exc()
            print("File not found")

        quit()

    main(args, loglevel)

if __name__ == '__main__':
    # Run setup if these files/directories don't already exist
    if (not os.path.exists(os.path.expanduser('~/.aws')) or not os.path.exists('.env')):
        os.system("bash setup.sh")

    parser = argparse.ArgumentParser(
        description="Create, deploy, query against models.",
        epilog="As an alternative to the commandline, params can be placed in a file, one per line, and specified on the commandline like '%(prog)s @params.conf'.",
        fromfile_prefix_chars='@')
    parser.add_argument(
        "--hf",
        help="Deploy a Hugging Face Model.",
        type=str
    )
    parser.add_argument(
        "--instance",
        help="EC2 instance type to deploy to.",
        type=str
    )
    parser.add_argument(
        "--deploy",
        help="path to YAML deployment configuration file",
        type=str
    )
    parser.add_argument(
        "--train",
        help="path to YAML training configuration file",
        type=str
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    
    parser.add_argument(
        "--cloud", 
        choices=['aws', 'gcp', 'azure'], 
        help="Specify the cloud provider for configuration and deployment"
    )
    args = parser.parse_args()

    cmd = ["bash", "scripts/preflight.sh"]
    if args.cloud:
        cmd.append(f"--cloud={args.cloud}")

    # Run the script
    subprocess.run(cmd, check=True)

    # Setup logging
    if args.verbose:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    if args.hf is not None:
        instance_type = args.instance or "ml.m5.xlarge"
        predictor = deploy_huggingface_model(args.hf, instance_type)
        quit()

    if args.deploy is not None:
        try:
            deployment = None
            model = None
            with open(args.deploy) as config:
                configuration = yaml.safe_load(config)
                deployment = configuration['deployment']

                # TODO: Support multi-model endpoints
                model = configuration['models'][0]
            deploy_model(deployment, model)
        except:
            traceback.print_exc()
            print("File not found")

        quit()

    if args.train is not None:
        try:
            train = None
            model = None
            with open(args.train) as config:
                configuration = yaml.safe_load(config)
                training = configuration['training']
                model = configuration['models'][0]
            fine_tune_model(training, model)
        except:
            traceback.print_exc()
            print("File not found")

        quit()

    from magemaker.main import main
    main(args, loglevel)
