#!/usr/bin/python3
"""Handle places rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_get(city_id):
    """get method to ret places by city id"""
    c_obj = storage.get(City, city_id)
    if not c_obj:
        abort(404)
    all_places = storage.all(Place)    
    places_cities= [obj.to_dict() for obj in all_places.values()
                    if obj.city_id == city_id]
    return jsonify(places_cities)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def place_id(city_id):
    """creates new place"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    req_data = request.get_json()
    if req_data is None:
        return jsonify({"error": "Not json"}), 400
    if req_data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400
    if req_data.get("user_id") is None:
        return jsonify({"error": "Missing user_id"}), 400
    u_obj = storage.get(User, req_data["user_id"])
    if not u_obj:
        abort(404)
    req_data['city_id'] = city_id
    new_city = City(**req_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'])
def place_getid(place_id):
    """get place by id"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_del(place_id):
    """delete place by id"""
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_put(place_id):
    """update place selected by id"""
    obj = storage.get(Place, place_id)
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
