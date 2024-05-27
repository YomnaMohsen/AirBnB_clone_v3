#!/usr/bin/python3
"""Handle states rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def state_get():
    """get method to ret states"""
    state_list = []
    state_dict = storage.all(State)
    for val in state_dict.values():
        state_list.append(val.to_dict())
    return jsonify(state_list)
       
    
@app_views.route('/states', methods=['POST'])
def state_post():
    req_data = request.get_json()
    if req_data is None:
        abort(400, "Not json")
    if req_data.get("name") is None:
        abort(400, "Missing name")
    new_state = State(**req_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201
    
    
@app_views.route('/states/<state_id>', methods=['GET'])
def state_id(state_id): 
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())
     
              

