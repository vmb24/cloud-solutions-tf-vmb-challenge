from repositories.equipment_health_repository import EquipmentHealthRepository

class EquipmentHealthUsecase:
    def __init__(self):
        self.equipment_health_repository = EquipmentHealthRepository()

    def create_equipment_health(self, data):
        return self.equipment_health_repository.create_equipment_health(data)

    def get_equipment_health(self, equipment_health_id):
        return self.equipment_health_repository.get_equipment_health(equipment_health_id)

    def update_equipment_health(self, equipment_health_id, data):
        self.equipment_health_repository.update_equipment_health(equipment_health_id, data)

    def delete_equipment_health(self, equipment_health_id):
        self.equipment_health_repository.delete_equipment_health(equipment_health_id)
