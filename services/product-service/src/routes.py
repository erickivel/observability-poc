
from views.ping_views import ping_bp
from views.products_view import products_bp

def register_views(app):
    app.register_blueprint(ping_bp)
    app.register_blueprint(products_bp)
