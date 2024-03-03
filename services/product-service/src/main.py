from flask import Flask 
from flask_cors import CORS
import logging
from logging.config import dictConfig

from src.routes import register_views

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.logger.setLevel(logging.INFO) 

register_views(app)

CORS(app)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',  port = 3002, debug = False)

