import marshmallow
import sqlalchemy.exc

from src.dao.role_dao import RoleDao
from src.dao.user_dao import UserDAO
from src.models.user import Role, role_schema


class RoleService:
    def __init__(self, role_dao: RoleDao, user_dao: UserDAO):
        self.role_dao = role_dao
        self.user_dao = user_dao

    def _validate_request_data(self, request_data: dict) -> tuple[bool, str | None]:
        try:
            role_schema.dump(request_data)
        except marshmallow.ValidationError as e:
            err = True
            return err, e.messages
        err = False
        return err, None

    def get_one(self, uuid: str) -> Role | None:
        return self.role_dao.get_one(uuid)

    def get_one_by_name(self, name: str) -> Role | None:
        return self.role_dao.get_one_by_name(name)

    def get_all(self) -> list[Role]:
        return self.role_dao.get_all()

    def create(self, request_data: dict) -> tuple[bool, Role | str]:
        err, msg = self._validate_request_data(request_data)
        if err:
            return err, msg
        role = Role(**request_data)
        try:
            err = False
            return err, self.role_dao.create(role)
        except sqlalchemy.exc.IntegrityError as e:
            err = True
            return err, str(e)

    def update(self, uuid: str, request_data: dict) -> tuple[bool, Role | str | None]:
        err, msg = self._validate_request_data(request_data)
        if err:
            return err, msg

        role = self.role_dao.get_one(uuid)
        if role:
            role.name = request_data['name']
            return err, self.role_dao.update(role)

        err = True
        return err, None

    def delete(self, uuid: str):
        role = self.get_one(uuid)
        if role:
            return self.role_dao.delete(role)
        return None

    def assign_role(self, user_id: str, role_id: str):
        role = self.role_dao.get_one(role_id)
        if not role:
            return None

        user = self.user_dao.get_user_by_uuid(user_id)
        if not user:
            return None

        user.roles.append(role)
        return self.user_dao.update(user)

    def remove_role(self, user_id: str, role_id: str):
        user = self.user_dao.get_user_by_uuid(user_id)
        if not user:
            return None

        for role in user.roles:
            if str(role.id) == role_id:
                user.roles.remove(role)
                return self.user_dao.update(user)
        return None
        