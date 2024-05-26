#!/usr/bin/python3
"""Handle states rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'DELETE','POST', 'PUT', ])
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'POST', 'PUT'])
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
        storage.save()
        return jsonify({})
    
    if request.method == 'POST':
        req_data = request.get_json()
        if req_data is None:
            abort(400, "Not json")
        if req_data.get("name") is None:
             abort(400, "Missing name")
        new_state = State(**req_data)
        new_state.save()
        return jsonify(new_state.to_dict(), 201)            
