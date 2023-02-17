import json

import marshmallow
import sqlalchemy.exc
from pydantic import ValidationError

from src.models.user import Role
from src.dao.role_dao import BaseRoleDAO
from src.models.user import role_schema


class RoleService:
    def __init__(self, user_dao: BaseRoleDAO):
        self.dao = user_dao

    def _validate_request_data(self, request_data: dict) -> tuple[bool, str | None]:
        try:
            role_schema.dump(request_data)
        except marshmallow.ValidationError as e:
            err = True
            return err, e.messages
        err = False
        return err, None

    def get_one(self, uuid: str) -> Role | None:
        return self.dao.get_one(uuid)

    def get_one_by_name(self, name: str) -> Role | None:
        return self.dao.get_one_by_name(name)

    def get_all(self) -> list[Role]:
        return self.dao.get_all()

    def create(self, request_data: dict) -> tuple[bool, Role | str]:
        err, msg = self._validate_request_data(request_data)
        if err:
            return err, msg
        role = Role(**request_data)
        try:
            err = False
            return err, self.dao.create(role)
        except sqlalchemy.exc.IntegrityError as e:
            err = True
            return err, str(e)

    def update(self, uuid: str, request_data: dict) -> tuple[bool, Role | str | None]:
        err, msg = self._validate_request_data(request_data)
        if err:
            return err, msg

        role = self.dao.get_one(uuid)
        if role:
            role.name = request_data['name']
            return err, self.dao.update(role)

        err = True
        return err, None

    def delete(self, uuid: str):
        role = self.get_one(uuid)
        if role:
            return self.dao.delete(role)
        return None
