import uuid

from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import UUID
from src.db import db

user_role = db.Table(
    'user_role',
    db.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    db.Column('user_id', UUID, db.ForeignKey('users.id')),
    db.Column('role_id', UUID, db.ForeignKey('roles.id'))
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    users = db.relationship('User', secondary=user_role, backref='roles')

    def __repr__(self):
        return f'<Role {self.name}>'


# serialization/deserialization


class RoleSchema(Schema):
    id = fields.UUID()
    name = fields.String()


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
