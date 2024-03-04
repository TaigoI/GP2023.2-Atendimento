from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/user')

from src.user import routes