import http

from flask import request
from flask_restx import Namespace, Resource, reqparse

from src.container import auth_service, user_dao

auth_ns = Namespace('api/v1/auth')


@auth_ns.route('/signup')
class SignUpView(Resource):
    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument(
            'login',
            type=str,
            required=True,
            help='Username to sign up'
        )
        parser.add_argument(
            'password',
            type=str,
            required=True,
            help='Password to sign up'
        )
        args = parser.parse_args()
        login = args['login']
        password = args['password']

        if user_dao.get_user(login):
            return {'message': 'User already exists'}, http.HTTPStatus.BAD_REQUEST

        auth_service.signup(login, password)

        return {'message': 'User created successfully'}, http.HTTPStatus.CREATED


@auth_ns.route('/login/oauth/<provider>/redirect')
class OauthSignUpView(Resource):
    @staticmethod
    def get(provider):
        auth_code_arg_names = {
            'yandex': 'code'
        }
        auth_code = ''

        for code in auth_code_arg_names.values():
            auth_code = request.args.get(code)
            if auth_code:
                break

        if not auth_code:
            return '', http.HTTPStatus.BAD_REQUEST

        oauth_result = auth_service.oauth_login(provider=provider, auth_code=auth_code)
        if not oauth_result:
            return {'message': f'Unable to authenticate using {provider}'}, http.HTTPStatus.UNAUTHORIZED


        return {'message': 'User created successfully'}, http.HTTPStatus.CREATED


@auth_ns.route('/login')
class LoginView(Resource):
    @staticmethod
    def post():
        login_parser = reqparse.RequestParser()
        login_parser.add_argument(
            'login',
            type=str,
            required=True,
            help='The user\'s login'
        )
        login_parser.add_argument(
            'password',
            type=str,
            required=True,
            help='The user\'s password'
        )

        args = login_parser.parse_args()
        login: str = args.get('login')
        password: str = args.get('password')

        authy = auth_service.login(login, password)
        if not authy:
            return {"message": "Incorrect username or password"}, http.HTTPStatus.UNAUTHORIZED
        return authy, http.HTTPStatus.OK


@auth_ns.route('/refresh')
class RefreshTokenView(Resource):
    @staticmethod
    def put():
        parser = reqparse.RequestParser()
        parser.add_argument(
            'refresh_token',
            type=str,
            required=True,
            help='Refresh token'
        )
        args = parser.parse_args()
        refresh_token = args['refresh_token']

        new_tokens = auth_service.get_refresh_token(refresh_token)
        if not new_tokens:
            return {'message': 'refresh token is invalid'}, http.HTTPStatus.FORBIDDEN

        return {'access_token': new_tokens[0], 'refresh_token': new_tokens[1]}, http.HTTPStatus.CREATED


@auth_ns.route('/logout')
class LogoutView(Resource):
    @staticmethod
    def delete():
        parser = reqparse.RequestParser()
        parser.add_argument(
            'access_token',
            type=str,
            required=True,
            help='Refresh token'
        )
        parser.add_argument(
            'refresh_token',
            type=str,
            required=True,
            help='Refresh token'
        )
        args = parser.parse_args()
        access_token = args['access_token']
        refresh_token = args['refresh_token']

        if not access_token or not refresh_token:
            return {'message': 'Access and refresh tokens are required.'}, http.HTTPStatus.NOT_FOUND

        auth_service.logout(access_token, refresh_token)

        return {'message': 'Logged out successfully.'}, http.HTTPStatus.OK


@auth_ns.route('/user_history')
class LoginHistory(Resource):
    @staticmethod
    def post():
        login_parser = reqparse.RequestParser()
        login_parser.add_argument(
            'login',
            type=str,
            required=True,
            help='The user\'s login'
        )
        args = login_parser.parse_args()
        login: str = args.get('login')

        user_history = auth_service.login_history(login)
        if not user_history:
            return {"message": "History user not found"}, http.HTTPStatus.NOT_FOUND
        return user_history, http.HTTPStatus.OK
