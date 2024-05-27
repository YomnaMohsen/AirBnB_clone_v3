#!/usr/bin/python3
"""Handle states rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_get():
    """get method to ret cities by state id"""
    state_list = []
    state_dict = storage.all(State)
    for val in state_dict.values():
        state_list.append(val.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_id(state_id):
    """post new state"""
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


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_getid(city_id):
    """get city by id"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_del(city_id):
    """delete city by id"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/cities/<city_id>', methods=['PUT'])
def city_put(city_id):
    """update city selected by id"""
    ignore_list = ["id", "updated_at", "created_at"]
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    req_data = request.get_json()
    if req_data is None:
        return jsonify({"error": "Not json"}), 400
    update_dict = {
        k: v for k, v in req_data.items() if k not in ignore_list
    }
    for key, val in update_dict.items():
        setattr(obj, key, val)
    storage.save()
    return jsonify(obj.to_dict()), 200
