import http

import pytest


@pytest.mark.asyncio
async def test_get_all_roles(aiohttp_session, make_get_request):
    endpoint = '/roles-management/'

    response = await make_get_request(endpoint)
    assert len(response['body']) == 2
    assert response['status'] == http.HTTPStatus.OK






