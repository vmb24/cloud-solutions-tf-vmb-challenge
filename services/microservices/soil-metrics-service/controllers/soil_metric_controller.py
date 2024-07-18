from flask import request, jsonify
from usecases.soil_metric_usecase import SoilMetricUsecase
from presenter.presenters_responses import response_with, success_response, error_response

class SoilMetricController:
    def __init__(self):
        self.soil_metric_usecase = SoilMetricUsecase()

    def create_soil_metric(self, data):
        try:
            data = request.get_json()
            soil_metric = self.soil_metric_usecase.create_soil_metric(data)
            return response_with(success_response(soil_metric)), 201
        except Exception as e:
            return response_with(error_response(str(e)))

    def get_soil_metric(self, soil_metric_id):
        try:
            soil_metric = self.soil_metric_usecase.get_soil_metric(soil_metric_id)
            return response_with(success_response(soil_metric)), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def update_soil_metric(self, soil_metric_id, data):
        try:
            self.soil_metric_usecase.update_soil_metric(soil_metric_id, data)
            return response_with(success_response({'message': 'Soil Metric updated'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def delete_soil_metric(self, soil_metric_id):
        try:
            self.soil_metric_usecase.delete_soil_metric(soil_metric_id)
            return response_with(success_response({'message': 'Soil Metric deleted'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500
