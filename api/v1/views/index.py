#!/usr/bin/python3
"""index file for json"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """method to get the status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def use_count():
    """use the newly added count() method from storage"""
    counts = {
        "users": storage.count("User"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "states": storage.count("State"),
    }
    return jsonify(counts)
