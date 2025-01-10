import unittest
import os
from dotenv import load_dotenv
from google.cloud import aiplatform
from google.api_core import exceptions as google_exceptions

# Import the function to be tested
from magemaker.gcp.delete_model import delete_vertex_ai_model

class TestDeleteVertexAIModelIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Setup method to load environment variables and perform initial setup
        """
        # Load environment variables
        load_dotenv()

        # Get required credentials and project details
        cls.project_id = os.getenv('PROJECT_ID')
        cls.location = os.getenv('GCLOUD_REGION')
        
        # Validate critical environment variables
        cls.assertIsNotNone(cls.project_id, "PROJECT_ID must be set in .env file")
        cls.assertIsNotNone(cls.location, "GCLOUD_REGION must be set in .env file")

        # Initialize Vertex AI
        aiplatform.init(project=cls.project_id, location=cls.location)

    def test_delete_nonexistent_endpoint(self):
        """
        Test attempting to delete a nonexistent endpoint
        """
        with self.assertRaises((google_exceptions.NotFound, google_exceptions.InvalidArgument)):
            # Use a predictable, but invalid endpoint name format
            nonexistent_endpoint_name = f"projects/{self.project_id}/locations/{self.location}/endpoints/invalid-endpoint-name"
            delete_vertex_ai_model(nonexistent_endpoint_name)

if __name__ == '__main__':
    unittest.main()