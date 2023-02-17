from src.dao.role_dao import RoleDao
from src.services.role_service import RoleService
from src.core.config import AppConfig
from src.db import db

app_config = AppConfig()

# MVC
role_dao = RoleDao(db.session)
role_service = RoleService(role_dao)
