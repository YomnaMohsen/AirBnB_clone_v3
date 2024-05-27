#!/usr/bin/python3
"""Handle states rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models import storage


@app_views.route('/states/cities/<city_id>/places', methods=['GET'])
def places_get(city_id):
    """get method to ret places by city id"""
    c_obj = storage.get(City, city_id)
    if not c_obj:
        abort(404)
    places_cities= [obj.to_dict() for obj in c_obj.places]
    return jsonify(places_cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def city_id(state_id):
    """creates new city"""
    req_data = request.get_json()
    if req_data is None:
        return jsonify({"error": "Not json"}), 400
    if req_data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400
    req_data['state_id'] = state_id
    new_city = City(**req_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


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
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
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
