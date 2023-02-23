import base64

from src.core.config import AppConfig, JWTSettings
from src.api.v1.dao.role_dao import RoleDao
from src.api.v1.dao.user_dao import UserDAO
from src.db import db
from src.api.v1.services.auth_service import AuthService
from src.api.v1.services.role_service import RoleService
from src.utills.security import PasswordHasher, TokenGenerator

app_config = AppConfig()
jwt_settings = JWTSettings()
token_generator = TokenGenerator(jwt_settings)
#print(token_generator.check_jwt_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dpbiI6InJ1c2xhbiIsInJvbGVzIjoiIiwiZXhwIjoxNjc3MTgyNzUxfQ.VtQ5LjXP9Xnk0acfDqOwVDO5FUXSyneZWz2GUovACPg'))
password_hasher = PasswordHasher()
print(base64.b64decode(password_hasher.hash_password('123')))

# MVC
role_dao = RoleDao(db.session)
user_dao = UserDAO(db.session)
auth_service = AuthService(user_dao, jwt_settings, token_generator, password_hasher)
role_service = RoleService(role_dao, user_dao)
