from repositories.crop_health_repository import CropHealthRepository

class CropHealthUsecase:
    def __init__(self):
        self.crop_health_repository = CropHealthRepository()

    def create_crop_health(self, data):
        return self.crop_health_repository.create_crop_health(data)

    def get_crop_health(self, crop_health_id):
        return self.crop_health_repository.get_crop_health(crop_health_id)

    def update_crop_health(self, crop_health_id, data):
        self.crop_health_repository.update_crop_health(crop_health_id, data)

    def delete_crop_health(self, crop_health_id):
        self.crop_health_repository.delete_crop_health(crop_health_id)
