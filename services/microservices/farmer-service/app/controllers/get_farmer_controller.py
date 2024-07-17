from flask import Blueprint, request, jsonify
from app.usecases.get_farmer import GetFarmer

get_farmer_controller = Blueprint('get_farmer_controller', __name__)
usecase = GetFarmer()

@get_farmer_controller.route('/farmer/<farmer_id>', methods=['GET'])
def get_farmer(farmer_id):
    return jsonify(usecase.get_farmer(farmer_id))