#!/bin/sh

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Logging functions
log_info() {
    echo "[INFO] $1"
}

log_debug() {
    echo "[DEBUG] $1"
}

log_error() {
    echo "[ERROR] $1" >&2
}

# Configuration functions
configure_aws() {
echo "Configuring AWS..."
echo "you need to create an aws user with access to Sagemaker"
echo "if you don't know how to do that follow this doc https://docs.google.com/document/d/1NvA6uZmppsYzaOdkcgNTRl7Nb4LbpP9Koc4H_t5xNSg/edit?usp=sharing"


# green
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

# echo green that press enter if you have already done this
echo -e "${GREEN}Press enter in the following configuration steps if you have already done this${NC}"

aws configure set region us-east-1 && aws configure
touch .env


if ! grep -q "SAGEMAKER_ROLE" .env
then
    # bash ./setup_role.sh
    bash "$SCRIPT_DIR/setup_role.sh"
fi
}


# GCP

configure_gcp() {
    echo "Configuring GCP..."
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

# echo "Setting up application default credentials..."
# gcloud auth application-default login --no-launch-browser

# if [ $? -ne 0 ]; then
#     echo -e "${RED}Failed to set application default credentials${NC}"
#     exit 1
# fi

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
}

# AZURE
configure_azure() {
echo "Configuring Azure..."
echo "Checking for Azure CLI installation..."
if ! command -v az &> /dev/null
then
    echo "Azure CLI not found. Installing..."
    OS="$(uname -s)"
    case "${OS}" in
        Linux*)     
            curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
            ;;
        Darwin*)    
            brew update && brew install azure-cli
            ;;
        *)          
            echo "Unsupported OS: ${OS}. See https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
            exit 1
            ;;
    esac
fi

# Check Azure login status
echo "Checking Azure login status..."
if ! az account show &> /dev/null; then
    echo "Not logged into Azure. Please log in..."
    az login
    if [ $? -ne 0 ]; then
        echo "Azure login failed. Please try again."
        exit 1
    fi
fi

# Get and set subscription
if ! grep -q "AZURE_SUBSCRIPTION_ID" .env; then
    SUBSCRIPTION_ID=$(az account show --query id -o tsv)
    if [ -n "$SUBSCRIPTION_ID" ]; then
        echo "AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID" >> .env
        export AZURE_SUBSCRIPTION_ID="$SUBSCRIPTION_ID"
        echo "Exported AZURE_SUBSCRIPTION_ID=${SUBSCRIPTION_ID}"
    else
        echo "No Azure subscription found"
        exit 1
    fi
fi

# Get and set resource group
if ! grep -q "AZURE_RESOURCE_GROUP" .env; then
    echo "Listing resource groups..."
    az group list -o table
    echo "Please enter the resource group name to use:"
    read RESOURCE_GROUP
    if [ -n "$RESOURCE_GROUP" ]; then
        echo "AZURE_RESOURCE_GROUP=$RESOURCE_GROUP" >> .env
        export AZURE_RESOURCE_GROUP="$RESOURCE_GROUP"
        echo "Exported AZURE_RESOURCE_GROUP=${RESOURCE_GROUP}"
    else
        echo "No resource group specified"
        exit 1
    fi
fi

# Get and set region
if ! grep -q "AZURE_REGION" .env; then
    CURRENT_REGION=$(az group show --name $AZURE_RESOURCE_GROUP --query location -o tsv)
    if [ -n "$CURRENT_REGION" ]; then
        echo "AZURE_REGION=$CURRENT_REGION" >> .env
        export AZURE_REGION="$CURRENT_REGION"
        echo "Exported AZURE_REGION=${CURRENT_REGION}"
    else
        echo "Available Azure regions:"
        az account list-locations --query "[].{Region:name}" -o table
        echo "Please enter the Azure region to use:"
        read AZURE_REGION
        echo "AZURE_REGION=$AZURE_REGION" >> .env
        export AZURE_REGION="$AZURE_REGION"
        echo "Exported AZURE_REGION=${AZURE_REGION}"
    fi
fi

# Check Azure ML workspace
echo "Checking Azure ML workspace..."
if ! grep -q "AZURE_WORKSPACE_NAME" .env; then
    # List available workspaces
    echo "Available Azure ML workspaces in resource group $AZURE_RESOURCE_GROUP:"
    az ml workspace list --resource-group $AZURE_RESOURCE_GROUP -o table
    
    echo "Please enter the Azure ML workspace name to use:"
    read WORKSPACE_NAME
    
    if [ -n "$WORKSPACE_NAME" ]; then
        # Verify workspace exists
        if az ml workspace show --name $WORKSPACE_NAME --resource-group $AZURE_RESOURCE_GROUP &> /dev/null; then
            echo "AZURE_WORKSPACE_NAME=$WORKSPACE_NAME" >> .env
            export AZURE_ML_WORKSPACE="$WORKSPACE_NAME"
            echo "Exported AZURE_WORKSPACE_NAME=${WORKSPACE_NAME}"
        else
            echo "Workspace $WORKSPACE_NAME not found in resource group $AZURE_RESOURCE_GROUP"
            exit 1
        fi
    else
        echo "No workspace specified"
        exit 1
    fi
fi

# Function to check and register Azure resource providers
check_and_register_providers() {
    local providers=(
        "Microsoft.MachineLearningServices"
        "Microsoft.ContainerRegistry"
        "Microsoft.KeyVault"
        "Microsoft.Storage"
        "Microsoft.Insights"
        "Microsoft.ContainerService"
        "Microsoft.PolicyInsights"
        "Microsoft.Cdn"
    )

    echo "Checking Azure resource providers..."
    for provider in "${providers[@]}"; do
        echo "Checking registration status for: $provider"
        
        # Get the registration state
        state=$(az provider show --namespace $provider --query registrationState -o tsv 2>/dev/null)
        
        if [ "$state" != "Registered" ]; then
            echo "$provider is not registered. Registering now..."
            az provider register --namespace $provider
            
            # Wait for registration to complete
            echo "Waiting for $provider registration to complete..."
            while true; do
                state=$(az provider show --namespace $provider --query registrationState -o tsv)
                if [ "$state" == "Registered" ]; then
                    echo "$provider registration completed"
                    break
                fi
                echo "Registration in progress... waiting 10 seconds"
                sleep 10
            done
        else
            echo "$provider is already registered"
        fi
    done
    
    echo "All required resource providers are registered"
}

# Add this line after the Azure login check
echo "Checking and registering required Azure resource providers..."
check_and_register_providers


# Verify all required Azure environment variables are set
echo "Verifying Azure environment variables..."
REQUIRED_VARS=("AZURE_SUBSCRIPTION_ID" "AZURE_RESOURCE_GROUP" "AZURE_REGION" "AZURE_WORKSPACE_NAME")
for var in "${REQUIRED_VARS[@]}"; do
    if ! grep -q "$var" .env; then
        echo "Missing required environment variable: $var"
        exit 1
    fi
done

echo "Azure environment setup completed successfully!"

# touch .env
}
configure_all_providers() {
    log_info "Performing comprehensive multi-cloud configuration..."
    
    
    # Detailed configuration for each cloud
    configure_aws
    configure_gcp
    configure_azure
    log_info "Multi-cloud configuration completed successfully"
}

# Argument parsing
CLOUD=""
while [ $# -gt 0 ]; do
    case "$1" in
        --cloud)
            shift
            CLOUD="$1"
            break
            ;;
        --cloud=*)
            CLOUD="${1#*=}"
            break
            ;;
    esac
    shift
done

# log_debug "Raw arguments: $@"
# log_debug "Cloud argument received: '$CLOUD'"

# Validate cloud argument
# validate_cloud_arg() {
#     case "$1" in
#         aws|gcp|azure)
#             return 0
#             ;;
#         *)
#             log_error "Invalid cloud provider: '$1'"
#             log_error "Supported providers: aws, gcp, azure"
#             exit 1
#             ;;
#     esac
# }

# Main configuration logic
main_configuration() {
    # Validate cloud argument
    # validate_cloud_arg "$CLOUD"
    
    # Configure specific cloud provider
    case "$CLOUD" in
        aws)
            configure_aws
            ;;
        gcp)
            configure_gcp
            ;;
        azure)
            configure_azure
            ;;
        all)
            configure_all_providers
            ;;
        *)
    esac
}

# Execute main configuration
main_configuration