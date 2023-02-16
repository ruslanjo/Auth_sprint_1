import uuid

from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db import db


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
        db.String,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String,
        nullable=False
    )

    def __repr__(self):
        return f'<User {self.login}>'


class LoginHistory(db.Model):
    __tablename__ = 'login_history'

    uuid = db.Column(
        db.String(36),
        primary_key=True
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(
            'users.id'
        )
    )
    timestamp = db.Column(
        db.DateTime,
        default=datetime.now()
    )

    user = relationship("User")
