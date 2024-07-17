from app.repositories.greenhouse_repository import GreenhouseRepository

class CreateGreenhouse:
    def __init__(self):
        self.repository = GreenhouseRepository()
        
    def create_greenhouse(self, data):
        return self.repository.create_greenhouse(data)
