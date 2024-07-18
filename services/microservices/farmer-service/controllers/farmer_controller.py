from flask import request, jsonify
from usecases.farmer_usecase import FarmerUsecase
from presenter.presenters_responses import response_with, success_response, error_response

class FarmerController:
    def __init__(self):
        self.farmer_usecase = FarmerUsecase()

    def create_farmer(self, data):
        try:
            data = request.get_json()
            farmer = self.farmer_usecase.create_farmer(data)
            return response_with(success_response(farmer)), 201
        except Exception as e:
            return response_with(error_response(str(e)))

    def get_farmer(self, farmer_id):
        try:
            farmer = self.farmer_usecase.get_farmer(farmer_id)
            return response_with(success_response(farmer)), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def update_farmer(self, farmer_id, data):
        try:
            self.farmer_usecase.update_farmer(farmer_id, data)
            return response_with(success_response({'message': 'Farmer updated'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def delete_farmer(self, farmer_id):
        try:
            self.farmer_usecase.delete_farmer(farmer_id)
            return response_with(success_response({'message': 'Farmer deleted'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500
