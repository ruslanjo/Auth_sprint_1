import http

import pytest


@pytest.mark.asyncio
async def test_get_all_roles(aiohttp_session, make_get_request):
    endpoint = '/roles-management/'

    response = await make_get_request(endpoint)
    assert len(response['body']) == 2
    assert response['status'] == http.HTTPStatus.OK


@pytest.mark.asyncio
async def test_create_role(aiohttp_session, make_post_request):
    endpoint = '/roles-management/'

    response = await make_post_request(endpoint, body={'name': 'test_role_3'})
    b = response['body']
    t = type(b)
    assert response['body']['name'] == 'test_role_3'
    assert response['status'] == http.HTTPStatus.CREATED

    # TODO добавить удаление созданной роли




