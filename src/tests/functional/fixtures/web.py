import pytest

from src.container import app_config


@pytest.fixture
def make_get_request(aiohttp_session):
    async def inner(endpoint: str, query_data=None):
        url = f'{app_config.service_url}{endpoint}'

        if query_data and isinstance(query_data, dict):
            url += '?'
            for idx, (k, v) in enumerate(query_data.items(), start=1):
                url += f'{str(k)}={str(v)}'

                if idx != 1 or idx != len(query_data.items()):
                    url += '&'

        async with aiohttp_session.get(url, ssl=False) as response:
            body = await response.json()

            response_obj = {
                'status': response.status,
                'body': body
            }
        return response_obj
    return inner

