import pytest
from unittest.mock import patch, MagicMock

# Assuming resources.py has a function named list_sagemaker_endpoints
from .resources import list_vertex_ai_endpoints


# @patch("ai_platform.Model")
# def test_list_vertex_ai_endpoints_no_filter(mock_boto_client):
#     ai_platform_mock = MagicMock()
#     ai_platform_mock.list.return_value = {
#         "Endpoints": [
#             {"EndpointName": "endpoint1"},
#             {"EndpointName": "endpoint2"},
#         ]
#     }
#     import pdb
#     pdb.set_trace()
#     mock_boto_client.return_value = ai_platform_mock

#     # endpoints = list_vertex_ai_endpoints()
#     # assert len(endpoints) == 2
#     # assert endpoints[0]['EndpointName'] == 'endpoint1'
#     # assert endpoints[1]['EndpointName'] == 'endpoint2'


def test_list_vertex_ai_endpoints():
    # actual call for quick testing
    endpoints = list_vertex_ai_endpoints()
    for endpoint in endpoints:
        assert "EndpointName" in endpoint
        assert "InstanceType" in endpoint

    # import pdb
    # pdb.set_trace()
    # only need EndpointName and InstanceType in the root dict
    # for endpoint in endpoints:
    #     assert "resource_name" in endpoints[0]
    #     assert "machine_type" in endpoints[0]

    