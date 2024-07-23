from flask import Flask, request, jsonify
from controllers.soil_metric_controller import SoilMetricController

app = Flask(__name__)
soil_metric_controller = SoilMetricController()

@app.route('/soil_metrics', methods=['POST'])
def create_soil_metric():
    return soil_metric_controller.create_soil_metric(request.json)

@app.route('/soil_metrics', methods=['GET'])
def get_soil_metrics():
    return soil_metric_controller.get_soil_metrics()

@app.route('/soil_metrics/<soil_metric_id>', methods=['GET'])
def get_soil_metric(soil_metric_id):
    return soil_metric_controller.get_soil_metric(soil_metric_id)

@app.route('/soil_metrics/<soil_metric_id>', methods=['PUT'])
def update_soil_metric(soil_metric_id):
    return soil_metric_controller.update_soil_metric(soil_metric_id, request.json)

@app.route('/soil_metrics/<soil_metric_id>', methods=['DELETE'])
def delete_soil_metric(soil_metric_id):
    return soil_metric_controller.delete_soil_metric(soil_metric_id)

if __name__ == '__main__':
    app.run(debug=True)
