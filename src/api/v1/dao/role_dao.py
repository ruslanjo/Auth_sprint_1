import abc

import sqlalchemy.exc
from flask_sqlalchemy.session import Session

from src.db import db
from src.models.user import Role


class BaseRoleDAO(abc.ABC):
    @abc.abstractmethod
    def get_one(self, uuid: str) -> db.Model | None:
        pass

    def get_one_by_name(self, name: str) -> db.Model | None:
        pass

    @abc.abstractmethod
    def get_all(self) -> list[db.Model]:
        pass

    @abc.abstractmethod
    def delete(self, uuid: str) -> None:
        pass

    @abc.abstractmethod
    def create(self, new_entity: db.Model) -> db.Model:
        pass

    @abc.abstractmethod
    def update(self, updated_entity: db.Model) -> db.Model:
        pass


class RoleDao(BaseRoleDAO):
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_one(self, uuid: str) -> Role | None:
        try:
            role = self.session.get(Role, uuid)
        except sqlalchemy.exc.DataError:
            return None
        return role

    def get_one_by_name(self, name: str) -> Role | None:
        role = self.session.query(Role).filter(Role.name == name).first()
        return role

    def get_all(self):
        return self.session.query(Role).all()

    def create(self, new_role: Role):
        self.session.add(new_role)
        self.session.commit()
        return new_role

    def delete(self, role_to_delete: Role):
        self.session.delete(role_to_delete)
        self.session.commit()
        return role_to_delete

    def update(self, role_updated: Role):
        return self.create(role_updated)