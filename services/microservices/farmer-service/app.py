from flask import Flask, request, jsonify
from controllers.farmer_controller import FarmerController

app = Flask(__name__)
farmer_controller = FarmerController()

@app.route('/farmers', methods=['POST'])
def create_farmer():
    return farmer_controller.create_farmer(request.json)

@app.route('/farmers/<farmer_id>', methods=['GET'])
def get_farmer(farmer_id):
    return farmer_controller.get_farmer(farmer_id)

@app.route('/farmers/<farmer_id>', methods=['PUT'])
def update_farmer(farmer_id):
    return farmer_controller.update_farmer(farmer_id, request.json)

@app.route('/farmers/<farmer_id>', methods=['DELETE'])
def delete_farmer(farmer_id):
    return farmer_controller.delete_farmer(farmer_id)

if __name__ == '__main__':
    app.run(debug=True)
