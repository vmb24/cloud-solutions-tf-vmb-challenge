from flask import request, jsonify
from usecases.crop_health_usecase import CropHealthUsecase
from presenter.presenters_responses import response_with, success_response, error_response

class CropHealthController:
    def __init__(self):
        self.crop_health_usecase = CropHealthUsecase()

    def create_crop_health(self, data):
        try:
            data = request.get_json()
            crop_health = self.crop_health_usecase.create_crop_health(data)
            return response_with(success_response(crop_health)), 201
        except Exception as e:
            return response_with(error_response(str(e)))

    def get_crop_health(self, crop_health_id):
        try:
            crop_health = self.crop_health_usecase.get_crop_health(crop_health_id)
            return response_with(success_response(crop_health)), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def update_crop_health(self, crop_health_id, data):
        try:
            self.crop_health_usecase.update_crop_health(crop_health_id, data)
            return response_with(success_response({'message': 'Crop Health updated'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def delete_crop_health(self, crop_health_id):
        try:
            self.crop_health_usecase.delete_crop_health(crop_health_id)
            return response_with(success_response({'message': 'Crop Health deleted'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500
