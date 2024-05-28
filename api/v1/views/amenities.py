#!/usr/bin/python3
"""Handle amenities rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'])
def ament_get():
    """get method to ret amenties"""
    am_list = []
    am_dict = storage.all(Amenity)
    for val in am_dict.values():
        am_list.append(val.to_dict())
    return jsonify(am_list)


@app_views.route('/amenities', methods=['POST'])
def ament_post():
    """post new amenity"""
    if request.content_type != 'application/json':
        return jsonify({"error": "Not json"}), 400
    req_data = request.get_json()
    if req_data is None:
        return jsonify({"error": "Not json"}), 400
    if req_data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400
    new_ament = Amenity(**req_data)
    storage.new(new_ament)
    storage.save()
    return jsonify(new_ament.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def ament_getid(amenity_id):
    """get amenity by id"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_del(amenity_id):
    """delete amenity by id"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def ament_put(amenity_id):
    """update amen selected by id"""
    obj = storage.get(Amenity, amenity_id)
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
