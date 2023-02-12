from flask_restx import Namespace, Resource
from flask import request

auth_ns = Namespace('auth')


@auth_ns.route('/signup')
class SignUpView(Resource):
    def post(self):
        data = request.json


@auth_ns.route('/login')
class LoginView(Resource):
    def post(self):
        return 'test'

