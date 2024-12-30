#!/bin/sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"



# AWS
echo "you need to create an aws user with access to Sagemaker"
echo "if you don't know how to do that follow this doc https://docs.google.com/document/d/1NvA6uZmppsYzaOdkcgNTRl7Nb4LbpP9Koc4H_t5xNSg/edit?usp=sharing"

# if ! command -v aws &> /dev/null
# then
#     OS="$(uname -s)"
#     case "${OS}" in
#         Linux*)     
#             curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#             unzip awscliv2.zip
#             sudo ./aws/install
#             ;;
#         Darwin*)    
#             curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
#             sudo installer -pkg AWSCLIV2.pkg -target /
#             ;;
#         *)          
#             echo "Unsupported OS: ${OS}. See https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
#             exit 1
#             ;;
#     esac
# fi

# aws configure set region us-east-1 && aws configure
# touch .env


# if ! grep -q "SAGEMAKER_ROLE" .env
# then
#     # bash ./setup_role.sh
#     bash "$SCRIPT_DIR/setup_role.sh"
# fi



# GCP
echo "you need to create a GCP service account with access to GCS and vertex ai"
echo "if you don't know how to do that follow this doc https://docs.google.com/document/d/1NvA6uZmppsYzaOdkcgNTRl7Nb4LbpP9Koc4H_t5xNSg/edit?usp=sharing"

if ! command -v gcloud &> /dev/null
then
    echo "you need to install gcloud sdk for the terminal"
    echo "https://cloud.google.com/sdk/docs/install"
fi

# only run this if the credentials are not set


echo "Checking for gcloud installation..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Please install the Google Cloud SDK first"
    exit 1
fi

echo "Checking for active gcloud accounts..."

# Get list of active accounts
ACCOUNTS=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null)

# Check if command was successful
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to retrieve account information${NC}"
    echo "Please check your gcloud installation"
    exit 1
fi

# Check if any accounts are found
if [ -z "$ACCOUNTS" ]; then
    echo -e "${YELLOW}No active gcloud accounts found${NC}"
    # echo "To login, use: gcloud auth login"
    gcloud auth login
    exit 0
fi

# Get current project ID
if ! grep -q "PROJECT_ID" .env
then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
    if [ -n "$PROJECT_ID" ]; then
        export PROJECT_ID="$PROJECT_ID"
        echo "PROJECT_ID=$PROJECT_ID" >> .env
        echo -e "${GREEN}Exported PROJECT_ID=${NC}${PROJECT_ID}"
    else
        echo -e "${YELLOW}No project currently set${NC}"
    fi
fi

if ! grep -q "GCLOUD_REGION" .env
then
    CURRENT_REGION=$(gcloud config get-value compute/region 2>/dev/null)
    if [ -n "$CURRENT_REGION" ]; then
        echo "GCLOUD_REGION=$CURRENT_REGION" >> .env
        export GCLOUD_REGION="$CURRENT_REGION"
        echo -e "${GREEN}Exported GCLOUD_REGION=${NC}${CURRENT_REGION}"
    else
        echo -e "${YELLOW}No compute region currently set${NC}"
    fi
fi

# touch .env

# if ! grep -q "GCS_BUCKET" .env
# then
#     bash "$SCRIPT_DIR/setup_gcp.sh"
# fi


