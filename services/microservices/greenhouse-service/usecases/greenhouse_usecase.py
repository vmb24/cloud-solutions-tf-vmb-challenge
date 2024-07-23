from repositories.greenhouse_repository import GreenhouseMetricRepository

class GreenhouseUsecase:
    def __init__(self):
        self.greenhouse_repository = GreenhouseMetricRepository()

    def create_greenhouse(self, data):
        return self.greenhouse_repository.create_greenhouse_metric(data)

    def get_greenhouse(self, greenhouse_id):
        return self.greenhouse_repository.get_greenhouse_metric(greenhouse_id)

    def update_greenhouse(self, greenhouse_id, data):
        self.greenhouse_repository.update_greenhouse_metric(greenhouse_id, data)

    def delete_greenhouse(self, greenhouse_id):
        self.greenhouse_repository.delete_greenhouse_metric(greenhouse_id)
