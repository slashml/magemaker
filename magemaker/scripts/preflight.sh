#!/bin/sh

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


echo "you need to create an aws use with access to Sagemaker"
echo "if you don't know how to do that follow this doc https://docs.google.com/document/d/1NvA6uZmppsYzaOdkcgNTRl7Nb4LbpP9Koc4H_t5xNSg/edit?usp=sharing"


if ! command -v aws &> /dev/null
then
    OS="$(uname -s)"
    case "${OS}" in
        Linux*)     
            curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
            unzip awscliv2.zip
            sudo ./aws/install
            ;;
        Darwin*)    
            curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
            sudo installer -pkg AWSCLIV2.pkg -target /
            ;;
        *)          
            echo "Unsupported OS: ${OS}. See https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
            exit 1
            ;;
    esac
fi
aws configure set region us-east-1 && aws configure
touch .env


if ! grep -q "SAGEMAKER_ROLE" .env
then
    # bash ./setup_role.sh
    bash "$SCRIPT_DIR/setup_role.sh"
fi