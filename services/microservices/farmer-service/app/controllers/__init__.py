from flask import Flask 
from app.controllers.create_farmer_controller import create_farmer_controller
from app.controllers.delete_farmer_controller import delete_farmer_controller
from app.controllers.get_farmer_controller import get_farmer_controller
from app.controllers.update_farmer_controller import update_farmer_controller

def create_app():
    app = Flask(__name__)
    app.register_blueprint(
        create_farmer_controller,
        delete_farmer_controller,
        get_farmer_controller,
        update_farmer_controller
    )
    return app