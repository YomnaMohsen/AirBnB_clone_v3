#!/usr/bin/python3
"""index module"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """return status code"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def ret_count():
    """endpoint retrieves the number of each objects by type:"""
    api_response = {}
    map_dict = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
        }
    for key, val in map_dict.items():
        api_response[val] = storage.count(key)
    return jsonify(api_response)
