from flask import Blueprint

bp = Blueprint('appointment_queue', __name__, url_prefix='/queue')

from src.appointment_queue import routes