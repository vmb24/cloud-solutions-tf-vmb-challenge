import unittest
from handlers.image_analysis_handler import ImageAnalysisHandler
from unittest.mock import patch, MagicMock

class ImageAnalysisHandlerTestCase(unittest.TestCase):
    @patch('boto3.client')
    def test_handle(self, mock_boto_client):
        mock_rekognition_client = MagicMock()
        mock_boto_client.return_value = mock_rekognition_client

        mock_rekognition_client.detect_labels.return_value = {
            'Labels': [{'Name': 'Label1', 'Confidence': 99.0}]
        }

        handler = ImageAnalysisHandler()
        event = {
            'Records': [{
                's3': {
                    'bucket': {'name': 'my-bucket'},
                    'object': {'key': 'image.jpg'}
                }
            }]
        }
        context = {}
        response = handler.handle(event, context)
        self.assertEqual(response['statusCode'], 200)

if __name__ == '__main__':
    unittest.main()
