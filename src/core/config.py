import pydantic
from pydantic import Field


class AppConfig(pydantic.BaseSettings):
    db_username: str = Field('app', env='POSTGRES_USERNAME')
    db_password: str = Field('123qwe', env='POSTGRES_PASSWORD')
    db_host: str = Field('localhost', env='POSTGRES_HOST')
    db_port: str = Field('5432', env='POSTGRES_PORT')
    db_name: str = Field('auth_service_db', env='AUTH_SERVICE_DB_NAME')
    a: str = str(db_port)

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'postgresql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    class Config:
        env_file = '../.environments.stage/.env.auth'

