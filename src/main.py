from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate

from src.container import app_config
from src.core.config import AppConfig
from src.utills.cli import register_cli
from src.db import db, init_db
from src.api.v1.views.auth_view import auth_ns
from src.api.v1.views.role_view import roles_management_ns

api = Api(title='Auth service', doc='/docs')
migrate = Migrate()


def create_app(config: AppConfig, rest_api: Api) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    register_extensions(application, rest_api)
    return application


def register_extensions(application: Flask, rest_api: Api):
    init_db(application)
    migrate.init_app(application, db)

    rest_api.init_app(application)
    rest_api.add_namespace(auth_ns)
    rest_api.add_namespace(roles_management_ns)


app = create_app(app_config, api)
register_cli(app, db)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
