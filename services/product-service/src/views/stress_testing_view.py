from flask import Blueprint, jsonify 
from flask import current_app as app
import time
from dotenv import load_dotenv
import os

stress_testing_bp = Blueprint('stress-testing', __name__, url_prefix="/stress-testing")

@stress_testing_bp.route('/long-runtime', methods=['GET'])
def long_runtime():
    load_dotenv()
    app.logger.info("Starting long runtime test")

    time.sleep(float(str(os.getenv("LONG_RUNTIME_TIME"))))

    app.logger.info("Ending long runtime test")
    return jsonify({"message": "Long runtime test finished successfully!"})

@stress_testing_bp.route('/error', methods=['GET'])
def trigger_error():
    app.logger.info("Starting error test")
    time.sleep(1)

    app.logger.error("Ending error test")
    return jsonify({"message": "Error test successfully triggered! XD"}), 500

@stress_testing_bp.route('/loop', methods=['GET'])
def loop():
    app.logger.info("Starting loop test")
    
    n = 1;
    while(True):
        n *= 2

    app.logger.info("Ending loop test")
    return jsonify({"message": "Loop test finished successfully!"})
