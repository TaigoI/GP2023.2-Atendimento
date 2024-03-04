from src.appointment_queue import bp

@bp.get('/')
def index():
    return "<h1>Queue's hello world</h1>"