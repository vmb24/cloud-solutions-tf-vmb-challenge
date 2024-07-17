from app.repositories.farmer_repository import FarmerRepository

class DeleteFarmer:
    def __init__(self):
        self.repository = FarmerRepository()
        
    def delete_farmer(self, farmer_id):
        return self.repository.delete_farmer(farmer_id)