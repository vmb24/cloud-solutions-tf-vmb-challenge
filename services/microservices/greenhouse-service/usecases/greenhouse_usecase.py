from repositories.greenhouse_repository import GreenhouseRepository

class GreenhouseUsecase:
    def __init__(self):
        self.greenhouse_repository = GreenhouseRepository()

    def create_greenhouse(self, data):
        return self.greenhouse_repository.create_greenhouse(data)

    def get_greenhouse(self, greenhouse_id):
        return self.greenhouse_repository.get_greenhouse(greenhouse_id)

    def update_greenhouse(self, greenhouse_id, data):
        self.greenhouse_repository.update_greenhouse(greenhouse_id, data)

    def delete_greenhouse(self, greenhouse_id):
        self.greenhouse_repository.delete_greenhouse(greenhouse_id)
