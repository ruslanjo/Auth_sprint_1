from flask_restx import Namespace, Resource, reqparse

from src.container import auth_service, user_dao

auth_ns = Namespace('auth')


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
            return {'message': 'User already exists'}, 400

        auth_service.signup(login, password)

        return {'message': 'User created successfully'}, 201


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
            return {"message": "Incorrect username or password"}, 401
        return authy, 200


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
            return {'message': 'refresh token is invalid'}, 403

        return new_tokens, 201


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
            return {'message': 'Access and refresh tokens are required.'}, 400

        auth_service.logout(access_token, refresh_token)

        return {'message': 'Logged out successfully.'}, 200
