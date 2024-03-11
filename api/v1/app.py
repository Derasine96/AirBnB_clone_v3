#!/usr/bin/python3
"""A script to return the status of your API"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import environ


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """Freeing up resources such as database connections"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors."""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
