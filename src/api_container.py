from dotenv import load_dotenv

from src.core.config import AppConfig, JWTSettings, OAuthConfig
from src.api.v1.dao.role_dao import RoleDao
from src.api.v1.dao.user_dao import UserDAO
from src.db import db
from src.api.v1.services.auth_service import AuthService
from src.api.v1.services.role_service import RoleService
from src.utills.security import PasswordHasher, TokenGenerator


app_config = AppConfig()
oauth_config = OAuthConfig()
jwt_settings = JWTSettings()

token_generator = TokenGenerator(jwt_settings)
password_hasher = PasswordHasher()

# MVC
role_dao = RoleDao(db.session)
user_dao = UserDAO(db.session)
auth_service = AuthService(user_dao, jwt_settings, token_generator, password_hasher)
role_service = RoleService(role_dao, user_dao)
