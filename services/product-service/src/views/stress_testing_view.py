from flask import Blueprint, jsonify 
import time
from dotenv import load_dotenv
import os

stress_testing_bp = Blueprint('stress-testing', __name__, url_prefix="/stress-testing")

@stress_testing_bp.route('/long-runtime', methods=['GET'])
def long_runtime():
    load_dotenv()
    print("Starting long runtime test")

    print("LONG RUNAD", os.getenv("LONG_RUNTIME_TIME"))
    time.sleep(float(str(os.getenv("LONG_RUNTIME_TIME"))))

    print("Ending long runtime test")
    return jsonify({"message": "Long runtime test finished successfully!"})

@stress_testing_bp.route('/error', methods=['GET'])
def trigger_error():
    print("Starting error test")
    time.sleep(1)

    print("Ending error test")
    return jsonify({"message": "Error test successfully triggered! XD"}), 500

@stress_testing_bp.route('/loop', methods=['GET'])
def loop():
    print("Starting loop test")
    
    n = 1;
    while(True):
        n *= 2


    print("Ending loop test")
    return jsonify({"message": "Loop test finished successfully!"})
