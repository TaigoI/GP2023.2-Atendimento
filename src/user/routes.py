from src.user import bp

@bp.route('/')
def index():
    return "<h1>User's hello world</h1>"