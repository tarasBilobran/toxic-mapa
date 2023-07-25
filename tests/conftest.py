import time
from pathlib import Path

import docker
import psycopg2
import pytest
import asyncpg

import alembic.command
import alembic.config

from app_context import default_app_context
from config import DBConfig

pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
def db_config():
    # overwrite default configuration to connect to test db
    return DBConfig(
        host="127.0.0.1",
        db="test",
        user="postgres",
        password="password",
        port="6666",
    )


@pytest.fixture(autouse=True)
async def app_context():
    async with default_app_context() as context:
        yield context


@pytest.fixture
async def db_conn(db_config, postgres_db):
    async with asyncpg.create_pool(
            host=db_config.host,
            port=db_config.port,
            user=db_config.user,
            password=db_config.password,
            database=db_config.db,
    ) as pool:
        async with pool.acquire() as conn:
            yield conn


@pytest.fixture
def postgres_db(postgres_instance, db_config):
    """Create test database. Apply migrations."""
    conn = psycopg2.connect(
        host=db_config.host,
        port=db_config.port,
        user=db_config.user,
        password=db_config.password,
        database='postgres',
    )
    conn.set_session(autocommit=True)

    try:
        alembic_ini = Path(__file__).parent.parent / 'alembic.ini'
        alembic_dir = alembic_ini.parent / "migrations"

        cursor = conn.cursor()
        cursor.execute("DROP database if exists test;")
        cursor.execute(f"CREATE DATABASE test;")
        _alembic = alembic.config.Config(str(alembic_ini))
        # Assumes that the Alembic root is the directory containing alembic.ini.
        _alembic.set_main_option("script_location", str(alembic_dir))
        connection_url = f"postgresql://postgres:password@127.0.0.1:6666/test"
        _alembic.set_main_option("sqlalchemy.url", connection_url)
        alembic.command.upgrade(_alembic, "head")
        yield
        cursor.execute("DROP database if exists test;")
    finally:
        conn.close()


@pytest.fixture()
async def prune_tables(db_conn):
    yield
    # prune all tables to avoid collision between tests
    await db_conn.execute(
        """
        DO $$DECLARE
        r RECORD;
        BEGIN
            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename != 'alembic_version') LOOP
                EXECUTE 'TRUNCATE TABLE v1.' || quote_ident(r.tablename) || ' CASCADE;';
            END LOOP;
        END$$;
        """
    )


@pytest.fixture
def postgres_instance():
    # Spin up PostgreSQL container that will be used by tests
    container_name = "db_for_testing"
    client = docker.DockerClient(timeout=5)
    containers = [container for container in client.containers.list() if container.name == container_name]
    if not containers:
        container = client.containers.create(
            "postgres:14",
            name=container_name,
            environment={"POSTGRES_USER": "postgres", "POSTGRES_PASSWORD": "password", "POSTGRES_DB": "postgres"},
            auto_remove=True,
            detach=True,
            ports={"5432/tcp": 6666},
        )
        container.start()
        # Give instance time to initialize
        time.sleep(2)
    yield