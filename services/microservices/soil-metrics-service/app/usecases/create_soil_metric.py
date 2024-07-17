from app.repositories.soil_metrics_repository import SoilMetricsRepository

class CreateSoilMetric:
    def __init__(self):
        self.repository = SoilMetricsRepository()

    def create_soil_metric(self, data):
        return self.repository.create_soil_metric(data)