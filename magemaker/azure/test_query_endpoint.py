
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import json
import dotenv


from .query_endpoint import query_vertexai_endpoint_rest

def test_query_endpoint_rest():
    import google.auth
    import google.auth.transport.requests
    import requests


    endpoint_id = '1234567890'
    input_text = 'This is a test'


    resp = query_vertexai_endpoint_rest(endpoint_id=endpoint_id, input_text=input_text)
