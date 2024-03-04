from flask import Blueprint

bp = Blueprint('appointment', __name__, url_prefix='/appointment')

from src.appointment import routes