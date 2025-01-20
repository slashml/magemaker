import pytest
from unittest.mock import patch, MagicMock

# Assuming resources.py has a function named list_sagemaker_endpoints
from .resources import list_vertex_ai_endpoints


def test_list_vertex_ai_endpoints():
    # actual call for quick testing
    endpoints = list_vertex_ai_endpoints()
    for endpoint in endpoints:
        assert "EndpointName" in endpoint
        assert "InstanceType" in endpoint
