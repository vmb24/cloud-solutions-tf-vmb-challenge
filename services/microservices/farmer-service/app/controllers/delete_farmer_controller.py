from flask import Blueprint, request, jsonify
from app.usecases.delete_farmer import DeleteFarmer

delete_farmer_controller = Blueprint('delete_farmer_controller', __name__)
usecase = DeleteFarmer()

@delete_farmer_controller.route('/farmer/<farmer_id>', methods=['DELETE'])
def delete_farmer(farmer_id):
    return jsonify(usecase.delete_farmer(farmer_id))