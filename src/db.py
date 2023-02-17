from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def init_db(application: Flask):
    db.init_app(application)
    from src.models.user import User, Role
