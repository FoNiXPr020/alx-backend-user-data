#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")


if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

if AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


if AUTH_TYPE == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def bef_req():
    """
    Filter each request before it's handled by the proper route
    """
    if auth is None:
        pass
    else:
        setattr(request, "current_user", auth.current_user(request))


@app.route('/users/me', methods=['GET'])
def me():
    """ Returns the authenticated user or 404
    """
    if request.current_user is None:
        abort(404)
    return jsonify(request.current_user.to_dict())


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Get user by id
    """
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_dict())
    return jsonify(User.find_by_id(user_id).to_dict())
