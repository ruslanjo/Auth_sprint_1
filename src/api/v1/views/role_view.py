import http
import json

from flask import request
from flask_restx import Namespace, Resource

from src.container import role_service
from src.models.user import role_schema, roles_schema
from src.utills.role_management import role_required

roles_management_ns = Namespace('api/v1/roles-management')
user_management_ns = Namespace('api/v1/user-management')


@roles_management_ns.route('/')
class RolesManagementView(Resource):
    @role_required({'superuser'})
    def get(self):
        roles = role_service.get_all()
        return roles_schema.dump(roles), http.HTTPStatus.OK

    @role_required({'superuser'})
    def post(self):
        request_data = request.json
        err, data = role_service.create(request_data)
        if err:
            return json.dumps({'message': 'resource was not created, wrong data passed'}), http.HTTPStatus.BAD_REQUEST
        return role_schema.dump(data), http.HTTPStatus.CREATED


@roles_management_ns.route('/<role_id>')
class RoleManagementView(Resource):
    @role_required({'superuser'})
    def get(self, role_id: str):
        role = role_service.get_one(role_id)
        if role:
            return role_schema.dump(role), http.HTTPStatus.OK
        return json.dumps({'message': 'resource not found'}), http.HTTPStatus.NOT_FOUND

    @role_required({'superuser'})
    def delete(self, role_id: str):
        role = role_service.delete(role_id)
        if role:
            return '', http.HTTPStatus.NO_CONTENT
        return json.dumps({'message': 'resource not found'}), http.HTTPStatus.NOT_FOUND

    @role_required({'superuser'})
    def put(self, role_id: str):
        req_data = request.json
        err, data = role_service.update(role_id, req_data)

        if err:
            return json.dumps({'message': 'update was not completed'}), http.HTTPStatus.BAD_REQUEST
        return role_schema.dump(data), http.HTTPStatus.OK


@roles_management_ns.route('/users/<user_id>')
class UserRoleManagementView(Resource):
    @role_required({'superuser'})
    def post(self, user_id: str):
        role_id = request.json.get('role_id')
        if role_id:
            result = role_service.assign_role(user_id, role_id)
            if result:
                return json.dumps(''), http.HTTPStatus.CREATED
        return json.dumps({'message': 'role was not assigned'}), http.HTTPStatus.BAD_REQUEST

    @role_required({'superuser'})
    def delete(self, user_id: str):
        role_id = request.json.get('role_id')
        if role_id:
            result = role_service.remove_role(user_id, role_id)
            if result:
                return json.dumps(''), http.HTTPStatus.NO_CONTENT
        return json.dumps({'message': 'role was not deleted'}), http.HTTPStatus.BAD_REQUEST
