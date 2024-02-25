from flask import Flask 
from flask_cors import CORS

from routes import register_views

app = Flask(__name__)

register_views(app)

CORS(app)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',  port = 3001, debug = False)

