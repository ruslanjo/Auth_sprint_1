import uuid
from datetime import datetime

from marshmallow import Schema, fields
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

from src.db import db

user_role = db.Table(
    'user_role',
    db.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False),
    db.Column('user_id', UUID, db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('role_id', UUID, db.ForeignKey('roles.id', ondelete='CASCADE'))
)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    login = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(70),
        nullable=False
    )

    def __repr__(self):
        return f'<User {self.login}>'


class UserSignIn(db.Model):
    __tablename__ = 'users_sign_in'
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
        }
    )
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(
            'users.id',
            ondelete='CASCADE'
        ),
        nullable=False,
    )
    timestamp = db.Column(
        db.DateTime,
        default=datetime.now()
    )
    user_agent = db.Column(
        db.Text
    )
    user_device_type = db.Column(
        db.Text,
        primary_key=True,
        default='web'
    )

    user = relationship("User", cascade='all, delete', passive_deletes=True)


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship('User', secondary=user_role, backref='roles', cascade='all, delete', passive_deletes=True)

    def __repr__(self):
        return f'<Role {self.name}>'


# serialization/deserialization


class RoleSchema(Schema):
    id = fields.UUID()
    name = fields.String()


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
