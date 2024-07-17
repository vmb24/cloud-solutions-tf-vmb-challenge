from app.repositories.farmer_repository import FarmerRepository

class UpdateFarmer:
    def __init__(self):
        self.repository = FarmerRepository()
    
    def update_farmer(self, data):
        return self.repository.update_farmer(data)