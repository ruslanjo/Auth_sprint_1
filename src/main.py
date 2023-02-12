from flask import Flask
from flask_restx import Api

from core.config import AppConfig
from views.auth_view import auth_ns
from src.db import db, init_db
from src.container import app_config

api = Api(title='Auth service', doc='/docs')


def create_app(config: app_config, rest_api: Api) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    register_extensions(application, rest_api)
    return application


def register_extensions(application: Flask, rest_api: Api):
    init_db(application)
    application.app_context().push()
    db.create_all()
    rest_api.init_app(application)
    rest_api.add_namespace(auth_ns)


app = create_app(app_config, api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
