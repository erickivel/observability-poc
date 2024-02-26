
from views.ping_views import ping_bp
from views.orders_view import orders_bp
from views.stress_testing_view import stress_testing_bp

def register_views(app):
    app.register_blueprint(ping_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(stress_testing_bp)
