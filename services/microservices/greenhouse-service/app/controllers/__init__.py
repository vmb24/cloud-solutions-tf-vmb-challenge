from flask import Flask 
from app.controllers.create_greenhouse_controller import create_greenhouse_controller
from app.controllers.delete_greenhouse_controller import delete_greenhouse_controller
from app.controllers.get_greenhouse_controller import get_greenhouse_controller
from app.controllers.update_greenhouse_controller import update_greenhouse_controller

def create_app():
    app = Flask(__name__)
    app.register_blueprint(
        create_greenhouse_controller,
        delete_greenhouse_controller,
        get_greenhouse_controller,
        update_greenhouse_controller
    )
    return app