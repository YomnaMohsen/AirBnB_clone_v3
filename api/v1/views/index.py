#!/usr/bin/python3
"""index module"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """return status code"""
    return jsonify({"status": "OK"})
