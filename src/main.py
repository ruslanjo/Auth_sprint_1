from flask import Flask
from flask_restx import Api

from src.core.config import AppConfig
from src.views.auth_view import auth_ns
from src.views.user_view import roles_management_ns
from src.db import db, init_db
from src.container import app_config

api = Api(title='Auth service', doc='/docs')


def create_app(config: AppConfig, rest_api: Api) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    register_extensions(application, rest_api)
    return application


def register_extensions(application: Flask, rest_api: Api):
    init_db(application)
    application.app_context().push()
    db.drop_all()
    db.create_all()

    rest_api.init_app(application)
    rest_api.add_namespace(auth_ns)
    rest_api.add_namespace(roles_management_ns)


app = create_app(app_config, api)

# user_1 = User(login='usermuser', password='123')
# role_1 = Role(name='cool guy')
# user_1.roles.append(role_1)
# db.session.add_all([user_1, role_1])
# db.session.commit()
#
# uu = db.session.query(User).first().id


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8080)
