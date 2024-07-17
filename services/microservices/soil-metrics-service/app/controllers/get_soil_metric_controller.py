from flask import Blueprint, request, jsonify
from app.usecases.get_soil_metric import GetSoilMetric

get_soil_metric_controller = Blueprint('get_soil_metric_controller', __name__)
usecase = GetSoilMetric()

@get_soil_metric_controller.route('/soil_metric/<soil_metric_id>', methods=['GET'])
def get_soil_metric(soil_metric_id):
    return jsonify(usecase.get_soil_metric(soil_metric_id))