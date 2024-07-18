from flask import Flask, request, jsonify
from controllers.greenhouse_controller import GreenhouseController

app = Flask(__name__)
greenhouse_controller = GreenhouseController()

@app.route('/greenhouses', methods=['POST'])
def create_farmer():
    return greenhouse_controller.create_farmer(request.json)

@app.route('/greenhouses/<farmer_id>', methods=['GET'])
def get_farmer(farmer_id):
    return greenhouse_controller.get_farmer(farmer_id)

@app.route('/greenhouses/<farmer_id>', methods=['PUT'])
def update_farmer(farmer_id):
    return greenhouse_controller.update_farmer(farmer_id, request.json)

@app.route('/greenhouses/<farmer_id>', methods=['DELETE'])
def delete_farmer(farmer_id):
    return greenhouse_controller.delete_farmer(farmer_id)

if __name__ == '__main__':
    app.run(debug=True)
