from app.repositories.greenhouse_repository import GreenhouseRepository

class GetGreenhouse:
    def __init__(self):
        self.repository = GreenhouseRepository()
        
    def get_greenhouse(self, greenhouse_id):
        return self.repository.get_greenhouse(greenhouse_id)