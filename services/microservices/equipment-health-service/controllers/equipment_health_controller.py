from flask import request, jsonify
from usecases.equipment_health_usecase import EquipmentHealthUsecase
from presenter.presenters_responses import response_with, success_response, error_response

class EquipmentHealthController:
    def __init__(self):
        self.equipment_health_usecase = EquipmentHealthUsecase()

    def create_equipment_health(self, data):
        try:
            data = request.get_json()
            equipment_health = self.equipment_health_usecase.create_equipment_health(data)
            return response_with(success_response(equipment_health)), 201
        except Exception as e:
            return response_with(error_response(str(e)))

    def get_equipment_health(self, equipment_health_id):
        try:
            equipment_health = self.equipment_health_usecase.get_equipment_health(equipment_health_id)
            return response_with(success_response(equipment_health)), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def update_equipment_health(self, equipment_health_id, data):
        try:
            self.equipment_health_usecase.update_equipment_health(equipment_health_id, data)
            return response_with(success_response({'message': 'Equipment Health updated'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def delete_equipment_health(self, equipment_health_id):
        try:
            self.equipment_health_usecase.delete_equipment_health(equipment_health_id)
            return response_with(success_response({'message': 'Equipment Health deleted'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500
