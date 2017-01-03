# -*- coding: utf-8 -*-
import os
import yaml

from functools import wraps
from flask import request, Response
from app import application as app


def load_credentials():
    root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
    creds_file = os.path.join(root_dir, 'creds.yml')
    with open(creds_file) as f:
        creds = yaml.load(f.read())
    app.config.update(creds)


def check_auth(username, password):
    """
    This function is called to check if a username /
    password combination is valid.
    """
    return username == app.config['ADMIN_USER'] and \
           password == app.config['ADMIN_PASS']


def authenticate():
    """
    Sends a 401 response that enables basic auth
    """
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
