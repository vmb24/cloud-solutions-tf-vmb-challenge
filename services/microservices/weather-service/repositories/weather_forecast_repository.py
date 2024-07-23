import boto3
from models.weather_forecast import WeatherForecast, WeatherForecastCreate

class WeatherForecastRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('WeatherForecast')

    def create_weather_forecast(self, data: WeatherForecastCreate):
        item = data.dict()
        self.table.put_item(Item=item)
        return item


    def get_weather_metric(self, weather_metric_id: str):
        response = self.table.get_item(Key={'id': weather_metric_id})
        return WeatherForecast(**response['Item'])

    def get_weather_metrics(self):
        response = self.table.scan()
        return [WeatherForecast(**item) for item in response['Items']]

    def update_weather_forecast(self, weather_forecast_id: str, data: WeatherForecastCreate):
        update_expression = "SET " + ", ".join([f"{k}=:{k}" for k in data.dict().keys()])
        expression_attribute_values = {f":{k}": v for k, v in data.dict().items()}
        response = self.table.update_item(
            Key={'id': weather_forecast_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response

    def delete_weather_forecast(self, weather_forecast_id: str):
        self.table.delete_item(Key={'id': weather_forecast_id})
