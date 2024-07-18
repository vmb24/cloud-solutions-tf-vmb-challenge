from flask import Flask, request, jsonify
from controllers.equipment_health_controller import EquipmentHealthController

app = Flask(__name__)
equipment_health_controller = EquipmentHealthController()

@app.route('/equipment_health', methods=['POST'])
def create_equipment_health():
    return equipment_health_controller.create_equipment_health(request.json)

@app.route('/equipment_health/<equipment_health_id>', methods=['GET'])
def get_equipment_health(equipment_health_id):
    return equipment_health_controller.get_equipment_health(equipment_health_id)

@app.route('/equipment_health/<equipment_health_id>', methods=['PUT'])
def update_equipment_health(equipment_health_id):
    return equipment_health_controller.update_equipment_health(equipment_health_id, request.json)

@app.route('/equipment_health/<equipment_health_id>', methods=['DELETE'])
def delete_equipment_health(equipment_health_id):
    return equipment_health_controller.delete_equipment_health(equipment_health_id)

if __name__ == '__main__':
    app.run(debug=True)
