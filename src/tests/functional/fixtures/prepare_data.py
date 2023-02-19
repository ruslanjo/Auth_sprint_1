import pytest

superuser_id = '189d5aac-92ca-465e-8eda-8220aa7dd162'
superuser_login = 'test_superuser_1'
superuser_password = 'password'

role_1_id = '1d355ac2-62b6-44b9-827c-080a0bc40841'
role_1_name = 'test purposes role 1'
role_2_id = 'e46c0d12-497b-485d-ac41-37a486c67dab'
role_2_name = 'test purposes role 2'


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
           ('{role_2_id}', '{role_2_name}')
    '''

    ur_id_1 = '5de1199b-362e-4b51-92e8-45a3209c4915'
    ur_id_2 = 'e8c95822-a1b0-40cd-8786-276a46b95220'
    fill_user_roles_query = f'''
    insert into user_role (id, user_id, role_id)
    values ('{ur_id_1}', '{superuser_id}', '{role_1_id}'),
           ('{ur_id_2}', '{superuser_id}', '{role_2_id}')
    '''
    postgres_cursor.execute(fill_roles_query)
    postgres_cursor.execute(fill_user_roles_query)
    postgres_conn.commit()


@pytest.fixture(scope='session', autouse=True)
def clean_data(postgres_cursor, postgres_conn):
    yield None
    delete_superuser_query = f'''
    delete from users
    where login = '{superuser_login}'
    '''
    delete_user_role_query = f'''
    delete from user_role
    where user_id = '{superuser_id}'
      and role_id in ('{role_1_id}', '{role_2_id}')
    '''
    delete_role_query = f'''
    delete from roles
    where id in ('{role_1_id}', '{role_2_id}')
    '''
    postgres_cursor.execute(delete_user_role_query)
    postgres_cursor.execute(delete_superuser_query)
    postgres_cursor.execute(delete_role_query)
    postgres_conn.commit()
