import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(application: Flask):
    db.init_app(application)
    from src.models.user import Role, User


class RedisConnection:
    def __init__(self):
        self.host = '0.0.0.0'
        self.port = 6379
        self.connection = redis.Redis(
            host=self.host,
            port=self.port,
        )

    def disconnect(self):
        self.connection.close()

    def get_key(self, key):
        return self.connection.get(key)

    def set_key(self, key, value, expire=None):
        self.connection.set(key, value, ex=expire)

    def delete_key(self, key):
        self.connection.delete(key)
