from app.repositories.farmer_repository import FarmerRepository

class CreateFarmer:
    def __init__(self):
        self.repository = FarmerRepository()
        
    def create_farmer(self, data):
        return self.repository.create_farmer(data)