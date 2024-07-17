from flask import Blueprint, request, jsonify
from app.usecases.delete_soil_metric import DeleteSoilMetric

delete_soil_metric_controller = Blueprint('delete_soil_metric_controller', __name__)
usecase = DeleteSoilMetric()

@delete_soil_metric_controller.route('/delete_soil_metric/<delete_soil_metric_id>', methods=['DELETE'])
def delete_soil_metric(soil_delete_soil_metric_id):
    return jsonify(usecase.delete_soil_metric(soil_delete_soil_metric_id))