
from views.ping_views import ping_bp
from views.products_view import products_bp
from views.product_orders_view import product_orders_bp
from views.stress_testing_view import stress_testing_bp

def register_views(app):
    app.register_blueprint(ping_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(product_orders_bp)
    app.register_blueprint(stress_testing_bp)
