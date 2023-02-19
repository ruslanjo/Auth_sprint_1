import http

import pytest
from src.tests.functional.settings.role_settings import role_1_id, role_2_id, superuser_id

roles_to_del = []


@pytest.mark.asyncio
async def test_get_all_roles(make_get_request):
    endpoint = '/roles-management/'

    response = await make_get_request(endpoint)
    assert len(response['body']) >= 2  # as we insert in fixture 2 rows in roles table
    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_create_role(make_post_request):
    endpoint = '/roles-management/'

    response = await make_post_request(endpoint, body={'name': 'test_create_role_role_name'})
    roles_to_del.append(response['body']['id'])
    assert response['body']['name'] == 'test_create_role_role_name'
    assert response['status'] == http.HTTPStatus.CREATED

    # TODO добавить удаление созданной роли


@pytest.mark.asyncio
async def test_get_role_by_id(make_get_request):
    endpoint = f'/roles-management/{role_1_id}'

    response = await make_get_request(endpoint)
    assert response['status'] == http.HTTPStatus.OK
    assert response['body']['id'] == role_1_id


@pytest.mark.asyncio
async def test_delete_role(make_delete_request):
    endpoint = f'/roles-management/{role_2_id}'
    response = await make_delete_request(endpoint)
    assert response['status'] == http.HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_update_role(make_put_request, make_get_request):
    endpoint = f'/roles-management/{role_1_id}'

    await make_put_request(endpoint, body={'name': 'updated name'})
    updated_role = await make_get_request(endpoint)
    assert updated_role['body']['name'] == 'updated name'


@pytest.mark.asyncio
async def test_assign_role(make_post_request):
    endpoint_assign = f'/roles-management/users/{superuser_id}'
    endpoint_create_role = '/roles-management/'

    create_role_response = await make_post_request(endpoint_create_role,
                                                   body={'name': 'test_assign_role'})
    new_role_id = create_role_response['body']['id']
    roles_to_del.append(new_role_id)
    assign_response = await make_post_request(endpoint_assign, body={'role_id': new_role_id})
    assert assign_response['status'] == http.HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_delete_role_from_user(make_post_request, make_delete_request):
    endpoint_role_user = f'/roles-management/users/{superuser_id}'
    endpoint_create_role = '/roles-management/'

    # creating role
    create_role_response = await make_post_request(endpoint_create_role, body={'name': 'test_role_to_delete'})
    new_role_id = create_role_response['body']['id']
    roles_to_del.append(new_role_id)

    #assigning role
    await make_post_request(endpoint_role_user, body={'role_id': new_role_id})
    # removing role from user
    delete_response = await make_delete_request(endpoint_role_user, body={'role_id': new_role_id})
    assert delete_response['status'] == http.HTTPStatus.NO_CONTENT


