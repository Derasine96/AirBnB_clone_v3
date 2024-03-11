#!/usr/bin/python3
"""a script that creates a new view for State objects that
    handles all default RESTFul API actions
"""
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views


def get_state_by_id(state_id):
    """Retrieve a state object by its ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return state


def get_city_by_id(state_id):
    """Retrieve a state object by its ID."""
    city = storage.get(City, state_id)
    if not city:
        abort(404)
    return city


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Returns the cities associated with a given state id."""
    state = get_state_by_id(state_id)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieve a City object by its ID."""
    city = get_city_by_id(city_id)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a city given its id."""
    city = get_city_by_id(city_id)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new city associated with the provided state."""
    get_state_by_id(state_id)
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    if 'name' not in http_body:
        abort(400, description='Missing name')
    city = City(**http_body)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Update the State object with all key-value pairs of the dictionary."""
    city = get_city_by_id(city_id)
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    filtered_body = {key: value for key, value in http_body.items()
                     if key not in ignore_keys}
    for key, value in filtered_body.items():
        setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
