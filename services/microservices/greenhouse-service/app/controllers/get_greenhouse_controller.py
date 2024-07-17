from flask import Blueprint, request, jsonify
from app.usecases.get_greenhouse import GetGreenhouse

get_greenhouse_controller = Blueprint('get_greenhouse_controller', __name__)
usecase = GetGreenhouse()

@get_greenhouse_controller.route('/greenhouse/<greenhouse_id>', methods=['GET'])
def get_greenhouse(greenhouse_id):
    return jsonify(usecase.get_greenhouse(greenhouse_id))