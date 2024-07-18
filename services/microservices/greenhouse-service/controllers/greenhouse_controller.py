from flask import request, jsonify
from usecases.greenhouse_usecase import GreenhouseUsecase
from presenter.presenters_responses import response_with, success_response, error_response

class GreenhouseController:
    def __init__(self):
        self.greenhouse_usecase = GreenhouseUsecase()

    def create_greenhouse(self, data):
        try:
            data = request.get_json()
            greenhouse = self.greenhouse_usecase.create_greenhouse(data)
            return response_with(success_response(greenhouse)), 201
        except Exception as e:
            return response_with(error_response(str(e)))

    def get_greenhouse(self, greenhouse_id):
        try:
            greenhouse = self.greenhouse_usecase.get_greenhouse(greenhouse_id)
            return response_with(success_response(greenhouse)), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def update_greenhouse(self, greenhouse_id, data):
        try:
            self.greenhouse_usecase.update_greenhouse(greenhouse_id, data)
            return response_with(success_response({'message': 'Greenhouse updated'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def delete_greenhouse(self, greenhouse_id):
        try:
            self.greenhouse_usecase.delete_greenhouse(greenhouse_id)
            return response_with(success_response({'message': 'Greenhouse deleted'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500
