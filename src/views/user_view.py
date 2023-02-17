import http
import json

from flask_restx import Namespace, Resource
from flask import, request

from src.container import role_service
from src.models.user import role_schema, roles_schema


roles_management_ns = Namespace('roles_management')


@roles_management_ns.route('/')
class RolesManagentView(Resource):
    def get(self):
        roles = role_service.get_all()
        return roles_schema.dump(roles), http.HTTPStatus.OK

    def post(self):
        request_data = request.json
        err, data = role_service.create(request_data)
        if err:
            return json.dumps({'message': 'resource was not created, wrong data passed'}), http.HTTPStatus.BAD_REQUEST
        return role_schema.dump(data), http.HTTPStatus.CREATED


@roles_management_ns.route('/<uuid>')
class RoleManagementView(Resource):
    def get(self, uuid: str):
        role = role_service.get_one(uuid)
        if role:
            return role_schema.dump(role), http.HTTPStatus.OK
        return json.dumps({'message': 'resource not found'}), http.HTTPStatus.NOT_FOUND

    def delete(self, uuid: str):
        role = role_service.delete(uuid)
        if role:
            return '', http.HTTPStatus.NO_CONTENT
        return json.dumps({'message': 'resource not found'}), http.HTTPStatus.NOT_FOUND

    def put(self, uuid: str):
        req_data = request.json
        err, data = role_service.update(uuid, req_data)

        if err:
            return json.dumps({'message': 'update was not completed'}), http.HTTPStatus.BAD_REQUEST
        return role_schema.dump(data), http.HTTPStatus.OK
