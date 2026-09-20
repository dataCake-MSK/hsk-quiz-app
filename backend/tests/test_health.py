from fastapi.testclient import TestClient

from app.infrastructure.config import Settings
from app.main import create_app
from tests.conftest import TEST_DATABASE_URL, requires_db


def _client(database_url: str | None = None) -> TestClient:
    settings = Settings(
        cors_origins=(),
        public_rate_limit="100/minute",
        auth_rate_limit="5/minute",
        database_url=database_url,
    )
    return TestClient(create_app(settings))


def test_health_returns_ok_without_db():
    response = _client().get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "not_configured"}


def test_health_reports_db_unavailable_when_connection_fails():
    # 존재하지 않는 포트 → 연결 실패지만 서버 자체는 응답해야 한다.
    response = _client("postgresql+psycopg://u:p@127.0.0.1:1/none").get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "unavailable"}


@requires_db
def test_health_reports_db_ok_with_real_db():
    response = _client(TEST_DATABASE_URL).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "ok"}
