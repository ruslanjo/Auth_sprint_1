import http

import pytest
from src.tests.functional.settings.role_settings import role_1_id, role_2_id


@pytest.mark.asyncio
async def test_get_all_roles(make_get_request):
    endpoint = '/roles-management/'

    response = await make_get_request(endpoint)
    assert len(response['body']) >= 2
    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_create_role(make_post_request):
    endpoint = '/roles-management/'

    response = await make_post_request(endpoint, body={'name': 'test_role_3'})
    b = response['body']
    t = type(b)
    assert response['body']['name'] == 'test_role_3'
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

    response = await make_put_request(endpoint, body={'name': 'updated name'})
    updated_role = await make_get_request(endpoint)
    assert updated_role['body']['name'] == 'updated name'
