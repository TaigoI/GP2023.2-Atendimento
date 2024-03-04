from src.appointment import bp

@bp.get('/')
def index():
    return "<h1>Appointment's hello world</h1>"