from src.dao.user_dao import UserDAO
from src.services.auth_service import AuthService
from src.core.config import AppConfig
from src.db import db
from src.core.config import JWTSettings
from src.utills.security import TokenGenerator, PasswordHasher

app_config = AppConfig()
jwt_settings = JWTSettings()
token_generator = TokenGenerator(jwt_settings)
password_hasher = PasswordHasher()

user_dao = UserDAO(db.session)
auth_service = AuthService(user_dao, jwt_settings, token_generator, password_hasher)
