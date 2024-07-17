from app.repositories.farmer_repository import FarmerRepository

class GetFarmer:
    def __init__(self):
        self.repository = FarmerRepository()
        
    def get_farmer(self, farmer_id):
        return self.repository.get_farmer(farmer_id)