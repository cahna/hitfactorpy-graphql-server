from pathlib import Path

import psycopg2
import pytest
from sqlalchemy.engine.url import URL, make_url


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    dc_file = Path(str(pytestconfig.rootdir)) / "tests" / "test_integration" / "docker-compose.yaml"
    assert dc_file.exists()
    return str(dc_file)


@pytest.fixture(scope="session")
def hitfactorpy_postgres_user() -> str:
    return "postgres"


@pytest.fixture(scope="session")
def hitfactorpy_postgres_password() -> str:
    return ""


@pytest.fixture(scope="session")
def hitfactorpy_postgres_port(docker_services):
    return docker_services.port_for("db_postgres", 5432)


@pytest.fixture(scope="session")
def hitfactorpy_postgres_database():
    return "hitfactorpy_graphql_server_test"


@pytest.fixture(scope="session")
def hitfactorpy_postgres_hostname(docker_ip, hitfactorpy_postgres_port) -> str:
    return f"{docker_ip}:{hitfactorpy_postgres_port}"


@pytest.fixture(scope="session")
def hitfactory_postgres_url(
    hitfactorpy_postgres_user,
    hitfactorpy_postgres_password,
    hitfactorpy_postgres_database,
    hitfactorpy_postgres_hostname,
):
    """Postgres URL without protocol prefix"""
    credentials = hitfactorpy_postgres_user + (
        f":{hitfactorpy_postgres_password}" if hitfactorpy_postgres_password else ""
    )
    return f"{credentials}@{hitfactorpy_postgres_hostname}/{hitfactorpy_postgres_database}"


def ping_postgres(db_url):
    conn = None
    try:
        parsed_url = make_url(db_url)
        conn = psycopg2.connect(
            database=parsed_url.database,
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.host,
            port=parsed_url.port,
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        return result and result[0] == 1
    except Exception:
        return False
    finally:
        if conn and hasattr(conn, "close"):
            conn.close()


@pytest.fixture(scope="session")
def postgres_service(docker_services, hitfactory_postgres_url):
    """Ensure that postgres is up and responsive"""
    url = f"postgresql://{hitfactory_postgres_url}"

    docker_services.wait_until_responsive(timeout=10.0, pause=0.1, check=lambda: ping_postgres(url))
    return make_url(url)
