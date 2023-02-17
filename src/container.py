from src.dao.user_dao import RoleDao
from src.services.user_service import RoleService
from src.core.config import AppConfig
from src.db import db
from src.models.user import RoleSchema

app_config = AppConfig()

# MVC
role_dao = RoleDao(db.session)
role_service = RoleService(role_dao)
