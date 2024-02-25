
from views.ping_views import ping_bp

def register_views(app):
    app.register_blueprint(ping_bp)
