#!/usr/bin/python3
"""a script that creates a new view for State objects that
    handles all default RESTFul API actions
"""
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.user import User
from models.city import City
from models import storage
from api.v1.views import app_views


def get_user_by_id(user_id):
    """Retrieve a user object by its ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return user


def get_city_by_id(city_id):
    """Retrieve a state object by its ID."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return city


def get_place_by_id(place_id):
    """Retrieve a state object by its ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Returns the places associated with a given citystate id."""
    city = get_city_by_id(city_id)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object by its ID."""
    place = get_place_by_id(place_id)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place given its id."""
    place = get_place_by_id(place_id)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a new place associated with the provided city."""
    city = get_city_by_id(city_id)
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    if 'user_id' not in http_body:
        abort(400, description='Missing user_id')
    user_id = http_body['user_id']
    user = get_user_by_id(user_id)
    if 'name' not in http_body:
        abort(400, description='Missing name')
    place = Place(**http_body)
    place.city_id = city_id
    place.user_id = user_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Update the State object with all key-value pairs of the dictionary."""
    place = get_place_by_id(place_id)
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    filtered_body = {key: value for key, value in http_body.items()
                     if key not in ignore_keys}
    for key, value in filtered_body.items():
        setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
