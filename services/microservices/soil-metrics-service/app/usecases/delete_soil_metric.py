from app.repositories.soil_metrics_repository import SoilMetricsRepository

class DeleteSoilMetric:
    def __init__(self):
        self.repository = SoilMetricsRepository()
        
    def delete_soil_metric(self, metric_id):
        return self.repository.delete_soil_metric(metric_id)