import pytest

from src.tests.functional.settings.role_settings import (superuser_id, superuser_password, superuser_login,
                                                         role_1_id, role_2_id, role_1_name, role_2_name)


def prepare_ids_in_query(ids: list) -> str:
    res = ""
    res += '('

    for idx, uuid in enumerate(ids, start=1):
        res += f"\'{uuid}\'"

        if idx != len(ids):
            res += ', '
    res += ')'
    return res


@pytest.fixture(scope='session', autouse=True)
def create_superuser(postgres_cursor, postgres_conn):
    create_superuser_query = f'''
        insert into users (id, login, password)
        values ('{superuser_id}', '{superuser_login}', '{superuser_password}')
        '''
    postgres_cursor.execute(create_superuser_query)
    postgres_conn.commit()


@pytest.fixture(scope='session', autouse=True)
def fill_roles(postgres_cursor, postgres_conn):
    fill_roles_query = f'''
    insert into roles (id, name)
    values ('{role_1_id}', '{role_1_name}'),
           ('{role_2_id}', '{role_2_name}'),
           ('{superuser_id}', 'superuser')
    '''

    ur_id_1 = '5de1199b-362e-4b51-92e8-45a3209c4915'
    ur_id_2 = 'e8c95822-a1b0-40cd-8786-276a46b95220'
    ur_id_3 = '70e1ea3a-af48-4792-8692-0da6a5f530df'
    fill_user_roles_query = f'''
    insert into user_role (id, user_id, role_id)
    values ('{ur_id_1}', '{superuser_id}', '{role_1_id}'),
           ('{ur_id_2}', '{superuser_id}', '{role_2_id}'),
           ('{ur_id_3}', '{superuser_id}', '{superuser_id}')
    '''
    postgres_cursor.execute(fill_roles_query)
    postgres_cursor.execute(fill_user_roles_query)
    postgres_conn.commit()


@pytest.fixture(scope='function', autouse=True)
def login_superuser(create_superuser, make_post_request):
    async def inner():
        payload = {'login': superuser_login,
                   'password': 'superuser'}
        endpoint = '/api/v1/auth/login'
        response = await make_post_request(endpoint, body=payload)
        return response['body']['access_token']
    return inner


@pytest.fixture(scope='session', autouse=True)
def clean_data(postgres_cursor, postgres_conn):
    yield None
    delete_superuser_query = f'''
    delete from users
    where login = '{superuser_login}'
    '''
    delete_user_role_query = f'''
    truncate table user_role cascade
    '''
    delete_role_query = f'''
    truncate table roles cascade
    '''
    postgres_cursor.execute(delete_user_role_query)
    postgres_cursor.execute(delete_superuser_query)
    postgres_cursor.execute(delete_role_query)
    postgres_conn.commit()