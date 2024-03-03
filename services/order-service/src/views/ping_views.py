from flask import Blueprint, jsonify
from flask import current_app as app

ping_bp = Blueprint('ping', __name__, url_prefix="/ping")

@ping_bp.route('/', methods=['GET'])
def ping():
    app.logger.info("Ping order service")
    message = {
        "ok": True
    }

    return jsonify(message)
