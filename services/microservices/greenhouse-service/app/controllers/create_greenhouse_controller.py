from flask import Blueprint, request, jsonify
from app.usecases.create_greenhouse import CreateGreenhouse

create_greenhouse_controller = Blueprint('create_greenhouse_controller', __name__)
usecase = CreateGreenhouse()

@create_greenhouse_controller.route('/greenhouse', methods=['POST'])
def create_greenhouse():
    data = request.json
    return jsonify(usecase.create_greenhouse(data))