from flask import Blueprint, request, jsonify
from app.usecases.update_soil_metric import UpdateSoilMetric

update_soil_metric_controller = Blueprint('update_soil_metric_controller', __name__)
usecase = UpdateSoilMetric()

@update_soil_metric_controller.route('/soil_metric', methods=['PUT'])
def update_soil_metric():
    data = request.json
    return jsonify(usecase.update_soil_metric(data))