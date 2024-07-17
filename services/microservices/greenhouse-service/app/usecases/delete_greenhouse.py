from app.repositories.greenhouse_repository import GreenhouseRepository

class DeleteGreenhouse:
    def __init__(self):
        self.repository = GreenhouseRepository()
    
    def delete_greenhouse(self, greenhouse_id):
        return self.repository.delete_greenhouse(greenhouse_id)