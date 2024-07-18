from repositories.soil_metric_repository import SoilMetricRepository

class SoilMetricUsecase:
    def __init__(self):
        self.soil_metric_repository = SoilMetricRepository()

    def create_soil_metric(self, data):
        return self.soil_metric_repository.create_soil_metric(data)

    def get_soil_metric(self, soil_metric_id):
        return self.soil_metric_repository.get_soil_metric(soil_metric_id)

    def update_soil_metric(self, soil_metric_id, data):
        self.soil_metric_repository.update_soil_metric(soil_metric_id, data)

    def delete_soil_metric(self, soil_metric_id):
        self.soil_metric_repository.delete_soil_metric(soil_metric_id)
