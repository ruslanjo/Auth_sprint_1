import pytest


@pytest.mark.asyncio
async def test_signup_success(make_post_request):
    payload = {'login': 'testuser', 'password': 'testpassword'}
    endpoint = '/auth/signup'
    response = await make_post_request(endpoint, body=payload)
    assert response['status'] == 201
    assert response['body'] == {'message': 'User created successfully'}


@pytest.mark.asyncio
async def test_signup_failure_user_exists(make_post_request):
    payload = {'login': 'testuser', 'password': 'testpassword'}
    endpoint = '/auth/signup'
    response = await make_post_request(endpoint, body=payload)
    assert response['status'] == 400
    assert response['body'] == {'message': 'User already exists'}


@pytest.mark.asyncio
async def test_signup_failure_missing_fields(make_post_request):
    payload = {'login': 'testuser'}
    endpoint = '/auth/signup'
    response = await make_post_request(endpoint, body=payload)
    assert response['status'] == 400


@pytest.mark.asyncio
async def test_login_success(make_post_request):
    payload = {'login': 'testuser', 'password': 'testpassword'}
    endpoint = '/auth/login'
    response = await make_post_request(endpoint, body=payload)
    assert response['status'] == 200
    assert response['body'].keys() == {'access_token', 'refresh_token'}


@pytest.mark.asyncio
async def test_login_failure_incorrect_password(make_post_request):
    payload = {'login': 'testuser', 'password': 'wrongpassword'}
    endpoint = '/auth/login'
    response = await make_post_request(endpoint, body=payload)
    assert response['status'] == 401
    assert response['body'] == {'message': 'Incorrect username or password'}


@pytest.mark.asyncio
async def test_login_failure_incorrect_username(make_post_request):
    payload = {'login': 'testluser', 'password': 'testpassword'}
    endpoint = '/auth/login'
    response = await make_post_request(endpoint, body=payload)

    assert response['status'] == 401
    assert response['body'] == {'message': 'Incorrect username or password'}


@pytest.mark.asyncio
async def test_refresh_success(make_put_request, make_post_request):
    endpoint_refresh = '/auth/refresh'
    endpoint_login = '/auth/login'
    payload = {'login': 'testuser', 'password': 'testpassword'}
    response = await make_post_request(endpoint_login, body=payload)
    refresh_token = response['body']['refresh_token']

    payload = {'refresh_token': refresh_token}
    response = await make_put_request(endpoint_refresh, payload)
    assert response['status'] == 201
    assert response['body'].keys() == {'access_token', 'refresh_token'}


@pytest.mark.asyncio
async def test_refresh_failure_invalid_token(make_put_request):
    endpoint_refresh = '/auth/refresh'
    payload = {'refresh_token': 'invalid_token'}
    response = await make_put_request(endpoint_refresh, body=payload)

    assert response['status'] == 403
    assert response['body'] == {'message': 'refresh token is invalid'}


@pytest.mark.asyncio
async def test_logout_success(make_delete_request, make_post_request):
    endpoint_logout = '/auth/logout'
    endpoint_login = '/auth/login'

    payload = {'login': 'testuser', 'password': 'testpassword'}
    response = await make_post_request(endpoint_login, body=payload)
    access_token = response['body']['access_token']
    refresh_token = response['body']['refresh_token']
    payload = {'access_token': access_token, 'refresh_token': refresh_token}
    response = await make_delete_request(endpoint_logout, body=payload)
    assert response['status'] == 200
    assert response['body'] == {'message': 'Logged out successfully.'}


@pytest.mark.asyncio
async def test_logout_failure_missing_tokens(make_delete_request):
    endpoint_logout = '/auth/logout'
    payload = {}
    response = await make_delete_request(endpoint_logout, body=payload)

    assert response['status'] == 400
    assert response['body']['message'] == 'Input payload validation failed'
