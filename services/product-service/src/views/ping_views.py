from flask import Blueprint, jsonify

ping_bp = Blueprint('ping', __name__, url_prefix="/ping")

@ping_bp.route('/', methods=['GET'])
def ping():
    message = {
        "ok": True
    }

    return jsonify(message)
