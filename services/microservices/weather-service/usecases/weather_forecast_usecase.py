from repositories.weather_forecast_repository import WeatherForecastRepository
from models.weather_forecast import WeatherForecast, WeatherForecastCreate

class WeatherForecastUsecase:
    def __init__(self):
        self.weather_forecast_repository = WeatherForecastRepository()

    def create_weather_forecast(self, data):
        return self.weather_forecast_repository.create_weather_forecast(data)

    def get_weather_metric(self, weather_metric_id: str):
        weather_metric = self.weather_forecast_repository.get_weather_metric(weather_metric_id)
        recommendation = self.get_recommendation(weather_metric)
        return {**weather_metric.dict(), "recommendation": recommendation}

    def get_weather_metrics(self):
        weather_metrics = self.weather_forecast_repository.get_weather_metrics()
        return [{"weather_metric": wm.dict(), "recommendation": self.get_recommendation(wm)} for wm in weather_metrics]

    def update_weather_forecast(self, weather_forecast_id, data):
        self.weather_forecast_repository.update_weather_forecast(weather_forecast_id, data)

    def delete_weather_forecast(self, weather_forecast_id):
        self.weather_forecast_repository.delete_weather_forecast(weather_forecast_id)

    def get_recommendation(self, weather_metric: WeatherForecast):
        event = {
            'weather_metric': weather_metric.dict()
        }
        response = self.lambda_client.invoke(
            FunctionName='WeatherRecommendations',
            InvocationType='RequestResponse',
            Payload=json.dumps(event)
        )
        response_payload = json.loads(response['Payload'].read())
        return response_payload['body']