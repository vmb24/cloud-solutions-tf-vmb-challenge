from app.repositories.soil_metrics_repository import SoilMetricsRepository

class UpdateSoilMetric:
    def __init__(self):
        self.repository = SoilMetricsRepository()
        
    def update_soil_metric(self, data):
        return self.repository.update_soil_metric(data)