#!/usr/bin/python3
"""a script that creates a new view for State objects that
    handles all default RESTFul API actions
"""
from flask import jsonify, abort, request, make_response
from models.user import User
from models import storage
from api.v1.views import app_views


def get_user_by_id(user_id):
    """Retrieve a state object by its ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return user


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects."""
    users = [user.to_dict()
             for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """Retrieve amenities by id."""
    user = get_user_by_id(user_id)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a state given its id."""
    user = get_user_by_id(user_id)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user from the data provided in the request body."""
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    if 'email' not in http_body:
        abort(400, description='Missing email')
    if 'password' not in http_body:
        abort(400, description='Missing password')
    user = User(**http_body)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Update the Amenity object with all key-value pairs of the dictionary."""
    user = get_user_by_id(user_id)
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    for key, value in http_body.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
