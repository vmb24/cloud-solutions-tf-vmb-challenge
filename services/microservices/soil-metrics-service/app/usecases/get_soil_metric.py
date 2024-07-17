from app.repositories.soil_metrics_repository import SoilMetricsRepository

class GetSoilMetric:
    def __init__(self):
        self.repository = SoilMetricsRepository()
    
    def get_soil_metric(self, metric_id):
        return self.repository.get_soil_metric(metric_id)