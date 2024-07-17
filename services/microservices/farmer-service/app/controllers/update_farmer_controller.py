from flask import Blueprint, request, jsonify
from app.usecases.update_farmer import UpdateFarmer

update_farmer_controller = Blueprint('update_farmer_controller', __name__)
usecase = UpdateFarmer()

@update_farmer_controller.route('/farmer', methods=['PUT'])
def update_farmer():
    data = request.json
    return jsonify(usecase.update_farmer(data))