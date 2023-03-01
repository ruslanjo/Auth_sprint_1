import http
import json
from functools import wraps
from flask import request


from src.api_container import token_generator


def unauthorized_response():
    return json.dumps({'message': 'denied'}), http.HTTPStatus.UNAUTHORIZED


def role_required(roles: set[str]):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if 'Authorization' not in request.headers:
                return unauthorized_response()
            token = request.headers['Authorization'].split('Bearer ')[-1]

            token_data = token_generator.check_jwt_token(token)
            if not token_data['result']:
                return unauthorized_response()

            if 'roles' not in token_data['data']:
                return json.dumps({'message': 'denied'}), http.HTTPStatus.UNAUTHORIZED
            users_roles = set(token_data['data']['roles'].split(', '))

            if users_roles.intersection(roles) or 'superuser' in users_roles:
                return func(*args, **kwargs)

        return inner
    return func_wrapper


