from flask import Blueprint, request, jsonify
from app.usecases.create_soil_metric import CreateSoilMetric

create_soil_metric_controller = Blueprint('create_soil_metric_controller', __name__)
usecase = CreateSoilMetric()

@create_soil_metric_controller.route('/soil_metric', methods=['POST'])
def create_soil_metric():
    data = request.json
    return jsonify(usecase.create_soil_metric(data))