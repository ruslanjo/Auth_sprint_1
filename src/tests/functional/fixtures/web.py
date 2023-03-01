import json

import aiohttp.client_exceptions

import pytest

from src.api_container import app_config


def configure_url_params(endpoint: str, query_data: dict = None):
    url = f'{app_config.service_url}{endpoint}'

    if query_data and isinstance(query_data, dict):
        url += '?'
        for idx, (k, v) in enumerate(query_data.items(), start=1):
            url += f'{str(k)}={str(v)}'

            if idx != 1 or idx != len(query_data.items()):
                url += '&'
    return url


@pytest.fixture
def make_get_request(aiohttp_session):
    async def inner(endpoint: str, query_data: dict = None, headers=None):
        url = configure_url_params(endpoint, query_data)
        if not headers:
            headers = {}

        async with aiohttp_session.get(url, ssl=False, headers=headers) as response:
            body = await response.json()

            response_obj = {
                'status': response.status,
                'body': body
            }
        return response_obj
    return inner


@pytest.fixture
def make_post_request(aiohttp_session):
    async def inner(endpoint: str, body: dict, query_data: dict = None, headers:    dict = None):
        url = configure_url_params(endpoint, query_data)

        if not headers:
            headers = {}

        async with aiohttp_session.post(url, json=body, ssl=False, headers=headers) as response:
            try:
                body = await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                try:
                    body = await response.text()
                except:
                    pass
            response_obj = {
                'status': response.status,
                'body': body
            }
        return response_obj
    return inner


@pytest.fixture
def make_delete_request(aiohttp_session):
    async def inner(endpoint: str, body: dict = None, query_data: dict = None, headers: dict = None):
        url = configure_url_params(endpoint, query_data)

        if not headers:
            headers = {}
        if not body:
            body = {}  # needed to pass to aiohttp delete request

        async with aiohttp_session.delete(url, json=body, ssl=False, headers=headers) as response:
            body = await response.json()
            response_obj = {
                'status': response.status,
                'body': body
            }
        return response_obj
    return inner


@pytest.fixture
def make_put_request(aiohttp_session):
    async def inner(endpoint: str, body: dict, query_data: dict = None, headers: dict = None):
        url = configure_url_params(endpoint, query_data)

        if not headers:
            headers = {}

        async with aiohttp_session.put(url, json=body, ssl=False, headers=headers) as response:
            body = await response.json()
            response_obj = {
                'status': response.status,
                'body': body
            }
        return response_obj
    return inner




