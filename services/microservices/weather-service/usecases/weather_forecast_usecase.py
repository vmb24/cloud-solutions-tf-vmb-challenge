from repositories.weather_forecast_repository import WeatherForecastRepository

class WeatherForecastUsecase:
    def __init__(self):
        self.weather_forecast_repository = WeatherForecastRepository()

    def create_weather_forecast(self, data):
        return self.weather_forecast_repository.create_weather_forecast(data)

    def get_weather_forecast(self, weather_forecast_id):
        return self.weather_forecast_repository.get_weather_forecast(weather_forecast_id)

    def update_weather_forecast(self, weather_forecast_id, data):
        self.weather_forecast_repository.update_weather_forecast(weather_forecast_id, data)

    def delete_weather_forecast(self, weather_forecast_id):
        self.weather_forecast_repository.delete_weather_forecast(weather_forecast_id)
