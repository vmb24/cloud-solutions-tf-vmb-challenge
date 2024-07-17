from flask import Flask 
from app.controllers.create_soil_metric_controller import create_soil_metric_controller
from app.controllers.delete_soil_metric_controller import delete_soil_metric_controller
from app.controllers.get_soil_metric_controller import get_soil_metric_controller
from app.controllers.update_soil_metric_controller import update_soil_metric_controller

def create_app():
    app = Flask(__name__)
    app.register_blueprint(
        create_soil_metric_controller,
        delete_soil_metric_controller,
        get_soil_metric_controller,
        update_soil_metric_controller
    )
    return app