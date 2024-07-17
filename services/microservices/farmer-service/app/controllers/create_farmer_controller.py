from flask import Blueprint, request, jsonify
from app.usecases.create_farmer import CreateFarmer

create_farmer_controller = Blueprint('create_farmer_controller', __name__)
usecase = CreateFarmer()

@create_farmer_controller.route('/farmer', methods=['POST'])
def create_farmer():
    data = request.json
    return jsonify(usecase.create_farmer(data))