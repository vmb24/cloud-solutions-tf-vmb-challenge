import unittest
from handlers.weather_recommendations_test import lambda_handler

class TestLambdaFunction(unittest.TestCase):
    def test_lambda_handler(self):
        event = {
            'soil_metric': {
                'ph': 6.5,
                'moisture': 30,
                'temperature': 22
            },
            'climate_data': {
                'region': 'North',
                'temperature': 25,
                'humidity': 60
            }
        }
        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('recommendation', json.loads(response['body']))

if __name__ == '__main__':
    unittest.main()
