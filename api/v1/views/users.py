#!/usr/bin/python3
"""Handle states rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
def user_get():
    """get method to ret users"""
    u_list = []
    u_dict = storage.all(User)
    for val in u_dict.values():
        u_list.append(val.to_dict())
    return jsonify(u_list)


@app_views.route('/users', methods=['POST'])
def user_post():
    """post user amenity"""
    req_data = request.get_json()
    if req_data is None:
        return jsonify({"error": "Not json"}), 400
        # abort(400, )
    if req_data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400
    new_ament = User(**req_data)
    storage.new(new_ament)
    storage.save()
    return jsonify(new_ament.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET'])
def user_getid(user_id):
    """get user by id"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def user_del(user_id):
    """delete user by id"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'])
def user_put(user_id):
    """update user selected by id"""
    ignore_list = ["id", "updated_at", "created_at"]
    obj = storage.get(User, user_id)
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
