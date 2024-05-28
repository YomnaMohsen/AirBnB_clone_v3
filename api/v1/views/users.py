#!/usr/bin/python3
"""Handle user rest apis"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def user_get():
    """get method to ret users"""
    u_list = []
    u_dict = storage.all(User)
    for val in u_dict.values():
        u_list.append(val.to_dict())
    return jsonify(u_list)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """post user amenity"""
    if request.content_type != 'application/json':
        return jsonify({"error": "Not json"}), 400
    req_data = request.get_json()
    if req_data is None:
        return jsonify({"error": "Not json"}), 400
        # abort(400, )
    if req_data.get("email") is None:
        return jsonify({"error": "Missing email"}), 400
    if req_data.get("password") is None:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**req_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_getid(user_id):
    """get user by id"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_del(user_id):
    """delete user by id"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """update user selected by id"""
    if request.content_type != 'application/json':
        return jsonify({"error": "Not json"}), 400
    obj = storage.get(User, user_id)
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
