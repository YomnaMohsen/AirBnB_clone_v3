#!/usr/bin/python3
"""Handle states rest apis"""
from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def state():
    state_list = []
    state_dict = storage.all(State)
    for val in state_dict.values():
        state_list.append(val.to_dict())
    return jsonify(state_list)
