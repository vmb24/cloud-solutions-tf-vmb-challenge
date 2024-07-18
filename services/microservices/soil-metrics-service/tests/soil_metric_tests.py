import unittest
from app import app

class SoilMetricTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_farmer(self):
        response = self.app.post('/farmers', json={
            "FarmerID": "1",
            "Name": "John Doe",
            "Email": "john@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_get_farmer(self):
        response = self.app.get('/farmers/1')
        self.assertEqual(response.status_code, 200)

    def test_update_farmer(self):
        response = self.app.put('/farmers/1', json={
            "Name": "John Doe Updated",
            "Email": "john_updated@example.com"
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_farmer(self):
        response = self.app.delete('/farmers/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
