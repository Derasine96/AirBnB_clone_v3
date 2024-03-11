#!/usr/bin/python3
"""a script that creates a new view for State objects that
    handles all default RESTFul API actions
"""
from flask import jsonify, abort, request, make_response
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


def get_amenity_by_id(amenity_id):
    """Retrieve a state object by its ID."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects."""
    amenities = [amenity.to_dict() for amenity in
                 storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Retrieve amenities by id."""
    amenity = get_amenity_by_id(amenity_id)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a state given its id."""
    amenity = get_amenity_by_id(amenity_id)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity from the data provided in the request body."""
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    if 'name' not in http_body:
        abort(400, description='Missing name')
    amenity = Amenity(**http_body)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Update the Amenity object with all key-value pairs of the dictionary."""
    amenity = get_amenity_by_id(amenity_id)
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    for key, value in http_body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 200)
