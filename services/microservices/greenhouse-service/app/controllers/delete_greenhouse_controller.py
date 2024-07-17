from flask import Blueprint, request, jsonify
from app.usecases.delete_greenhouse import DeleteGreenhouse

delete_greenhouse_controller = Blueprint('delete_greenhouse_controller', __name__)
usecase = DeleteGreenhouse()

@delete_greenhouse_controller.route('/greenhouse/<greenhouse_id>', methods=['DELETE'])
def delete_greenhouse(greenhouse_id):
    return jsonify(usecase.delete_greenhouse(greenhouse_id))