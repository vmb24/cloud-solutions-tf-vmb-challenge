from flask import request, jsonify
from usecases.weather_forecast_usecase import WeatherForecastUsecase
from presenter.presenters_responses import response_with, success_response, error_response

class WeatherForecastController:
    def __init__(self):
        self.weather_forecast_usecase = WeatherForecastUsecase()

    def create_weather_forecast(self, data):
        try:
            data = request.get_json()
            weather_forecast = self.weather_forecast_usecase.create_weather_forecast(data)
            return response_with(success_response(weather_forecast)), 201
        except Exception as e:
            return response_with(error_response(str(e)))

    def get_weather_forecast(self, weather_forecast_id):
        try:
            weather_forecast = self.weather_forecast_usecase.get_weather_forecast(weather_forecast_id)
            return response_with(success_response(weather_forecast)), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def update_weather_forecast(self, weather_forecast_id, data):
        try:
            self.weather_forecast_usecase.update_weather_forecast(weather_forecast_id, data)
            return response_with(success_response({'message': 'Weather forecast updated'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500

    def delete_weather_forecast(self, weather_forecast_id):
        try:
            self.weather_forecast_usecase.delete_weather_forecast(weather_forecast_id)
            return response_with(success_response({'message': 'Weather forecast deleted'})), 200
        except Exception as e:
            return response_with(error_response(str(e))), 500
