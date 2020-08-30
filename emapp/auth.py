from functools import wraps
from flask import current_app, request
from flask_restful import abort


def auth_simple_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('x-simple-auth')
        if current_app.config['API_KEY'] == token:
            return func(*args, **kwargs)
        abort(401)
    return wrapper
