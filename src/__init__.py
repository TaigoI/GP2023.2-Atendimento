from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    from src.appointment import bp as appointment
    app.register_blueprint(appointment)

    from src.appointment_queue import bp as appointment_queue
    app.register_blueprint(appointment_queue)

    from src.user import bp as user
    app.register_blueprint(user)

    return app