from flask import Blueprint, request, jsonify
from app.usecases.update_greenhouse import UpdateGreenhouse

update_greenhouse_controller = Blueprint('update_greenhouse_controller', __name__)
usecase = UpdateGreenhouse()

@update_greenhouse_controller.route('/greenhouse', methods=['PUT'])
def update_greenhouse():
    data = request.json
    return jsonify(usecase.update_greenhouse(data))