#!/usr/bin/python3
"""Handle states rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state_get():
    """get method to ret states"""
    state_list = []
    state_dict = storage.all(State)
    for val in state_dict.values():
        state_list.append(val.to_dict())
    return jsonify(state_list)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """post new state"""
    if request.content_type != 'application/json':
        return jsonify({"error": "Not json"}), 400
    req_data = request.get_json()
    if req_data is None:
        return jsonify({"error": "Not json"}), 400
        # abort(400, )
    if req_data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**req_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_getid(state_id):
    """get state by id"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def state_del(state_id):
    """delete state by id"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):
    """update state selected by id"""
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    if request.content_type != 'application/json':
        return jsonify({"error": "Not json"}), 400

    req_data = request.get_json()

    if req_data is None:
        return jsonify({"error": "Not json"}), 400

    ignore_list = ["id", "updated_at", "created_at"]
    update_dict = {
        k: v for k, v in req_data.items() if k not in ignore_list
    }
    for key, val in update_dict.items():
        setattr(obj, key, val)
    storage.save()
    return jsonify(obj.to_dict()), 200
