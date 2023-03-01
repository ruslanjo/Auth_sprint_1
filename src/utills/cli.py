import click

import sqlalchemy.exc
from flask import Flask

from src.models.user import Role, User
from src.api_container import password_hasher


def register_cli(application: Flask, db_obj):
    @application.cli.command('create-user')
    @click.argument('name')
    @click.argument('password')
    @click.argument('role_name')
    def create_user(name: str, password: str, role_name: str) -> None:
        user = User(login=name, password=password_hasher.hash_password(password).decode('utf-8'))
        role = db_obj.session.query(Role).filter(Role.name == role_name).first()
        if not role:
            print('There is no such role in DB, creating role')
            role = Role(name=role_name)
        user.roles.append(role)
        db_obj.session.add(user)
        db_obj.session.add(role)
        try:
            db_obj.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(str(e))
