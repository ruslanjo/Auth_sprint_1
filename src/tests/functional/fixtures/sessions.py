import asyncio

import psycopg2
import pytest
import aiohttp

from src.container import app_config


@pytest.fixture(scope='session', autouse=True)
async def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def aiohttp_session():
    session = aiohttp.ClientSession(trust_env=True)
    yield session
    await session.close()


@pytest.fixture(scope='session', autouse=True)
def postgres_conn():
    dsn = {
        'dbname': app_config.db_name,
        'user': app_config.db_username,
        'password': app_config.db_password,
        'host': app_config.db_host,
        'port': app_config.db_port,
    }
    conn = psycopg2.connect(**dsn)
    yield conn
    conn.close()


@pytest.fixture(scope='session', autouse=True)
def postgres_cursor(postgres_conn):
    cur = postgres_conn.cursor()
    yield cur
    cur.close()
