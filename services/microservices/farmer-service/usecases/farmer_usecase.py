from repositories.farmer_repository import FarmerRepository

class FarmerUsecase:
    def __init__(self):
        self.farmer_repository = FarmerRepository()

    def create_farmer(self, data):
        return self.farmer_repository.create_farmer(data)

    def get_farmer(self, farmer_id):
        return self.farmer_repository.get_farmer(farmer_id)

    def update_farmer(self, farmer_id, data):
        self.farmer_repository.update_farmer(farmer_id, data)

    def delete_farmer(self, farmer_id):
        self.farmer_repository.delete_farmer(farmer_id)
