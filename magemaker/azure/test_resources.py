import pytest
from unittest.mock import patch, MagicMock

# Assuming resources.py has a function named list_sagemaker_endpoints
from .resources import list_azure_endpoints

def test_list_azure_endpoints():
    # actual call for quick testing
    endpoints = list_azure_endpoints()

    print(endpoints)

    # only need EndpointName and InstanceType in the root dict
    for endpoint in endpoints:
        assert "InstanceType" in endpoint
        assert "EndpointName" in endpoint

    assert 2==1

    