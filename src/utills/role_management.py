import http
import json
from functools import wraps
from flask import request


from src.container import token_generator


def unauthorized_response():
    return json.dumps({'message': 'denied'}), http.HTTPStatus.UNAUTHORIZED


def role_required(roles: list[str]):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if 'access_token' not in request.headers:
                return unauthorized_response()

            token_data = token_generator.check_jwt_token(request.headers['access_token'])
            if not token_data['result']:
                return unauthorized_response()

            if 'role' not in token_data:
                return json.dumps({'message': 'denied'}), http.HTTPStatus.UNAUTHORIZED

            if token_data['role'] in roles or token_data['role'] == 'superuser':
                return func(*args, **kwargs)

        return inner
    return func_wrapper


