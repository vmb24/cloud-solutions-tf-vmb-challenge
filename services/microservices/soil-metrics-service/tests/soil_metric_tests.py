import unittest
from unittest.mock import patch
from usecases.soil_metrics_usecase import SoilMetricsUsecase
from models.soil_metric import SoilMetricCreate

class TestSoilMetricsUsecase(unittest.TestCase):
    @patch('usecases.soil_metrics_usecase.SoilMetricsRepository')
    def setUp(self, MockRepository):
        self.repo = MockRepository()
        self.usecase = SoilMetricsUsecase()

    @patch('usecases.soil_metrics_usecase.SoilMetricsUsecase.get_jurassic2_response')
    def test_create_soil_metric(self, mock_get_jurassic2_response):
        mock_get_jurassic2_response.return_value = "Recomendação gerada"
        data = SoilMetricCreate(ph=6.5, moisture=30, temperature=25)
        result = self.usecase.create_soil_metric(data)
        self.assertIn('recommendation', result)

if __name__ == '__main__':
    unittest.main()
