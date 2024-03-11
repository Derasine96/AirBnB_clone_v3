#!/usr/bin/python3
"""a script that creates a new view for State objects that
    handles all default RESTFul API actions
"""
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.user import User
from models.review import Review
from models import storage
from api.v1.views import app_views


def get_user_by_id(user_id):
    """Retrieve a user object by its ID."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return user


def get_place_by_id(place_id):
    """Retrieve a state object by its ID."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return place


def get_review_by_id(review_id):
    """Retrieve a state object by its ID."""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Returns the reviews associated with a given place id."""
    place = get_place_by_id(place_id)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews),


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieve a Review object by its ID."""
    review = get_review_by_id(review_id)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review given its id."""
    review = get_review_by_id(review_id)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new review associated with the provided place."""
    place = get_place_by_id(place_id)
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    if 'user_id' not in http_body:
        abort(400, description='Missing user_id')
    user_id = http_body['user_id']
    user = get_user_by_id(user_id)
    if 'text' not in http_body:
        abort(400, description='Missing text')
    review = Review(**http_body)
    review.place_id = place_id
    review.user_id = user_id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Update the Review object with all key-value pairs of the dictionary."""
    review = get_review_by_id(review_id)
    http_body = request.get_json()
    if not http_body:
        abort(400, description='Not a JSON')
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    filtered_body = {key: value for key, value in http_body.items()
                     if key not in ignore_keys}
    for key, value in filtered_body.items():
        setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
