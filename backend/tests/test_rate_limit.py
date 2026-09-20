from fastapi.testclient import TestClient

from app.infrastructure.config import Settings
from app.main import create_app


def _client(public_rate_limit: str = "3/minute") -> TestClient:
    settings = Settings(
        cors_origins=(),
        public_rate_limit=public_rate_limit,
        auth_rate_limit="5/minute",
    )
    return TestClient(create_app(settings))


def test_requests_within_limit_succeed():
    client = _client("3/minute")

    for _ in range(3):
        assert client.get("/health").status_code == 200


def test_request_over_limit_returns_429():
    client = _client("3/minute")
    for _ in range(3):
        client.get("/health")

    response = client.get("/health")

    assert response.status_code == 429
    assert "잠시 후" in response.json()["detail"]


def test_limit_counter_is_per_app():
    """앱을 새로 만들면 카운터도 새로 시작한다(테스트 간 간섭 방지)."""
    first = _client("1/minute")
    first.get("/health")
    assert first.get("/health").status_code == 429

    second = _client("1/minute")
    assert second.get("/health").status_code == 200
