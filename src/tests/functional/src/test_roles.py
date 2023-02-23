import http

import pytest

from src.tests.functional.settings.role_settings import (role_1_id, role_2_id,
                                                         superuser_id, superuser_login, superuser_password)


@pytest.mark.asyncio
async def test_get_all_roles(make_get_request, login_superuser):
    endpoint = '/api/v1/roles-management/'

    token = await login_superuser()
    response = await make_get_request(endpoint, headers={'Authorization': f'Bearer {token}'})
    assert len(response['body']) >= 2  # as we insert in fixture 2 rows in roles table
    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_create_role(make_post_request, login_superuser):
    endpoint = '/api/v1/roles-management/'

    token = await login_superuser()
    response = await make_post_request(endpoint,
                                       body={'name': 'test_create_role_role_name'},
                                       headers={'Authorization': f'Bearer {token}'})
    assert response['body']['name'] == 'test_create_role_role_name'
    assert response['status'] == http.HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_get_role_by_id(make_get_request, login_superuser):
    endpoint = f'/api/v1/roles-management/{role_1_id}'

    token = await login_superuser()
    response = await make_get_request(endpoint,
                                      headers={'Authorization': f'Bearer {token}'})
    assert response['status'] == http.HTTPStatus.OK
    assert response['body']['id'] == role_1_id


@pytest.mark.asyncio
async def test_delete_role(make_delete_request, login_superuser):
    endpoint = f'/api/v1/roles-management/{role_2_id}'
    token = await login_superuser()
    response = await make_delete_request(endpoint,
                                         headers={'Authorization': f'Bearer {token}'})
    assert response['status'] == http.HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_update_role(make_put_request, make_get_request, login_superuser):
    endpoint = f'/api/v1/roles-management/{role_1_id}'

    token = await login_superuser()

    await make_put_request(endpoint,
                           body={'name': 'updated name'},
                           headers={'Authorization': f'Bearer {token}'})
    updated_role = await make_get_request(endpoint,
                                          headers={'Authorization': f'Bearer {token}'})
    assert updated_role['body']['name'] == 'updated name'


@pytest.mark.asyncio
async def test_assign_role(make_post_request, login_superuser):
    endpoint_assign = f'/api/v1/roles-management/users/{superuser_id}'
    endpoint_create_role = '/api/v1/roles-management/'

    token = await login_superuser()
    create_role_response = await make_post_request(endpoint_create_role,
                                                   body={'name': 'test_assign_role'},
                                                   headers={'Authorization': f'Bearer {token}'})
    new_role_id = create_role_response['body']['id']
    assign_response = await make_post_request(endpoint_assign,
                                              body={'role_id': new_role_id},
                                              headers={'Authorization': f'Bearer {token}'})
    assert assign_response['status'] == http.HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_delete_role_from_user(make_post_request, make_delete_request, login_superuser):
    endpoint_role_user = f'/api/v1/roles-management/users/{superuser_id}'
    endpoint_create_role = '/api/v1/roles-management/'

    token = await login_superuser()
    # creating role
    create_role_response = await make_post_request(endpoint_create_role,
                                                   body={'name': 'test_role_to_delete'},
                                                   headers={'Authorization': f'Bearer {token}'})
    new_role_id = create_role_response['body']['id']

    #assigning role
    await make_post_request(endpoint_role_user,
                            body={'role_id': new_role_id},
                            headers={'Authorization': f'Bearer {token}'})
    # removing role from user
    delete_response = await make_delete_request(endpoint_role_user,
                                                body={'role_id': new_role_id},
                                                headers={'Authorization': f'Bearer {token}'})
    assert delete_response['status'] == http.HTTPStatus.NO_CONTENT


