from flask import Flask, request, jsonify
from controllers.crop_health_controller import CropHealthController

app = Flask(__name__)
crop_health_controller = CropHealthController()

@app.route('/crop_health', methods=['POST'])
def create_crop_health():
    return crop_health_controller.create_crop_health(request.json)

@app.route('/crop_health/<crop_health_id>', methods=['GET'])
def get_crop_health(crop_health_id):
    return crop_health_controller.get_crop_health(crop_health_id)

@app.route('/crop_health/<crop_health_id>', methods=['PUT'])
def update_crop_health(crop_health_id):
    return crop_health_controller.update_crop_health(crop_health_id, request.json)

@app.route('/crop_health/<crop_health_id>', methods=['DELETE'])
def delete_crop_health(crop_health_id):
    return crop_health_controller.delete_crop_health(crop_health_id)

if __name__ == '__main__':
    app.run(debug=True)
