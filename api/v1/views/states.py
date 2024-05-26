#!/usr/bin/python3
"""Handle states rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'DELETE','POST', 'PUT', ])
@app_views.route('/states/<state_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def state(state_id=None):
    if request.method == 'GET':
        if state_id is None:
            state_list = []
            state_dict = storage.all(State)
            for val in state_dict.values():
                state_list.append(val.to_dict())
            return jsonify(state_list)
        else:
            obj = storage.get(State, state_id)
            if not obj:
                abort(404)
            return jsonify(obj.to_dict())
    if request.method == 'DELETE':
        obj = storage.get(State, state_id)
        if not obj:
            abort(404)
        storage.delete(obj)
        return jsonify({})       
