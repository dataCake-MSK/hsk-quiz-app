from fastapi.testclient import TestClient

from app.infrastructure.config import Settings, _parse_origins
from app.main import create_app

ALLOWED = "http://localhost:8081"
DISALLOWED = "https://evil.example.com"


def _client(origins: tuple[str, ...]) -> TestClient:
    settings = Settings(
        cors_origins=origins,
        public_rate_limit="100/minute",
        auth_rate_limit="5/minute",
    )
    return TestClient(create_app(settings))


def test_preflight_from_allowed_origin_is_permitted():
    client = _client((ALLOWED,))

    response = client.options(
        "/health",
        headers={
            "Origin": ALLOWED,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.headers.get("access-control-allow-origin") == ALLOWED


def test_preflight_from_disallowed_origin_has_no_cors_header():
    client = _client((ALLOWED,))

    response = client.options(
        "/health",
        headers={
            "Origin": DISALLOWED,
            "Access-Control-Request-Method": "GET",
        },
    )

    assert "access-control-allow-origin" not in response.headers


def test_no_cors_header_when_origins_not_configured():
    client = _client(())

    response = client.get("/health", headers={"Origin": ALLOWED})

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_parse_origins_splits_and_trims():
    assert _parse_origins(" http://a , https://b ") == ("http://a", "https://b")
    assert _parse_origins("") == ()
    assert _parse_origins(None) == ()
