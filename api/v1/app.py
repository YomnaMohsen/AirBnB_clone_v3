#!/usr/bin/python3
"""flask app module that integrates html templates"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

# setting env var
host = os.getenv("HBNB_API_HOST", '0.0.0.0')
port = os.getenv("HBNB_API_PORT", '5000')

# global var app
app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
