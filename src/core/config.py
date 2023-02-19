import pydantic
from pydantic import Field


class JWTSettings(pydantic.BaseSettings):
    access_token_lifetime: int = Field(default=600, env='JWT_ACCESS_LIFETIME')
    refresh_token_lifetime: int = Field(default=86400, env='JWT_REFRESH_LIFETIME')


class RedisSettings(pydantic.BaseSettings):
    host: str = Field(default='127.0.0.1', env='REDIS_HOST')
    port: int = Field(default=6379, env='REDIS_PORT')


class AppConfig(pydantic.BaseSettings):
    db_username: str = Field('app', env='POSTGRES_USERNAME')
    db_password: str = Field('123qwe', env='POSTGRES_PASSWORD')
    db_host: str = Field('localhost', env='POSTGRES_HOST')
    db_port: str = Field('5432', env='POSTGRES_PORT')
    db_name: str = Field('auth_service_db', env='AUTH_SERVICE_DB_NAME')

    service_url: str = 'http://localhost:8080'

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'postgresql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    class Config:
        env_file = '../.environments.stage/.env.auth'
