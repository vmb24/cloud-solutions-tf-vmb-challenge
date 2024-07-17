from app.repositories.greenhouse_repository import GreenhouseRepository

class UpdateGreenhouse:
    def __init__(self):
        self.repository = GreenhouseRepository()
        
    def update_greenhouse(self, data):
        return self.repository.update_greenhouse(data)