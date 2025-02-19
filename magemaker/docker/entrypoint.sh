#!/bin/bash
set -e

# Setup AWS credentials if mounted
if [ -f "/root/.aws/credentials" ]; then
    export AWS_SHARED_CREDENTIALS_FILE="/root/.aws/credentials"
fi

# Setup GCP credentials if mounted
if [ -f "/root/.config/gcloud/application_default_credentials.json" ]; then
    export GOOGLE_APPLICATION_CREDENTIALS="/root/.config/gcloud/application_default_credentials.json"
fi

exec "$@"