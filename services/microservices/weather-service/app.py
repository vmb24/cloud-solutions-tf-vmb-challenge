from flask import Flask, request, jsonify
from controllers.weather_forecast_controller import WeatherForecastController

app = Flask(__name__)
weather_forecast_controller = WeatherForecastController()

@app.route('/weather_forecasts', methods=['POST'])
def create_weather_forecast():
    return weather_forecast_controller.create_weather_forecast(request.json)

@app.route('/', methods=['GET'])
def get_weather_metrics():
    result = weather_forecast_controller.get_weather_forecasts()
    return jsonify(result), 200

@app.route('/weather_forecasts/<weather_forecast_id>', methods=['GET'])
def get_weather_forecast(weather_forecast_id):
    return weather_forecast_controller.get_weather_forecast(weather_forecast_id)

@app.route('/weather_forecasts/<weather_forecast_id>', methods=['PUT'])
def update_weather_forecast(weather_forecast_id):
    return weather_forecast_controller.update_weather_forecast(weather_forecast_id, request.json)

@app.route('/weather_forecasts/<weather_forecast_id>', methods=['DELETE'])
def delete_weather_forecast(weather_forecast_id):
    return weather_forecast_controller.delete_weather_forecast(weather_forecast_id)

if __name__ == '__main__':
    app.run(debug=True)
