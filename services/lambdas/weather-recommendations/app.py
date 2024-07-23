from handlers.weather_recommendations_handler import WeatherRecommendationsHandler

def lambda_handler(event, context):
    handler = WeatherRecommendationsHandler()
    return handler.lambda_handler(event, context)
