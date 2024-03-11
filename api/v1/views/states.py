#!/usr/bin/python3
"""a script that creates a new view for State objects that
    handles all default RESTFul API actions
"""
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage
from api.v1.views import app_views


def get_state_by_id(state_id):
    """Retrieve a state object by its ID."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return state


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects."""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """Retrieve states by id."""
    state = get_state_by_id(state_id)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state given its id."""
    state = get_state_by_id(state_id)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state from the data provided in the request body."""
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    if 'name' not in http_body:
        abort(400, description='Missing name')
    state = State(**http_body)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update the State object with all key-value pairs of the dictionary."""
    state = get_state_by_id(state_id)
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    for key, value in http_body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
