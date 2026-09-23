"""회원가입 API (SRS-010)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, text

from app.infrastructure.config import Settings
from app.main import create_app
from tests.conftest import TEST_DATABASE_URL, requires_db

VALID = {"email": "mint@example.com", "password": "hsk-quiz-1234", "nickname": "민트"}


def _client(auth_rate_limit: str = "100/minute") -> TestClient:
    settings = Settings(
        cors_origins=(),
        public_rate_limit="100/minute",
        auth_rate_limit=auth_rate_limit,
        database_url=TEST_DATABASE_URL,
    )
    return TestClient(create_app(settings))


@requires_db
def test_register_returns_201_without_password_hash(db_engine: Engine):
    response = _client().post("/auth/register", json=VALID)

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"user_id", "email", "nickname"}
    assert body["email"] == VALID["email"]
    assert body["nickname"] == VALID["nickname"]
    assert isinstance(body["user_id"], int)


@requires_db
def test_password_is_stored_as_argon2_hash(db_engine: Engine):
    _client().post("/auth/register", json=VALID)

    with db_engine.connect() as connection:
        stored = connection.execute(text("SELECT password_hash FROM users")).scalar_one()

    assert stored.startswith("$argon2id$")
    assert VALID["password"] not in stored


@requires_db
def test_duplicate_email_returns_409(db_engine: Engine):
    client = _client()
    client.post("/auth/register", json=VALID)

    response = client.post("/auth/register", json=VALID)

    assert response.status_code == 409
    assert "이미" in response.json()["detail"]


@requires_db
def test_duplicate_email_with_different_case_returns_409(db_engine: Engine):
    client = _client()
    client.post("/auth/register", json=VALID)

    response = client.post("/auth/register", json={**VALID, "email": "MINT@Example.com"})

    assert response.status_code == 409


@requires_db
def test_email_is_stored_in_lowercase(db_engine: Engine):
    _client().post("/auth/register", json={**VALID, "email": "MiNt@Example.COM"})

    with db_engine.connect() as connection:
        stored = connection.execute(text("SELECT email FROM users")).scalar_one()

    assert stored == "mint@example.com"


@pytest.mark.parametrize(
    "payload",
    [
        {**VALID, "password": "1234567"},  # 8자 미만
        {**VALID, "email": "not-an-email"},
        {**VALID, "nickname": ""},
        {"email": VALID["email"], "password": VALID["password"]},  # nickname 누락
    ],
    ids=["short-password", "bad-email", "empty-nickname", "missing-nickname"],
)
@requires_db
def test_invalid_payload_returns_422(db_engine: Engine, payload: dict[str, str]):
    response = _client().post("/auth/register", json=payload)

    assert response.status_code == 422


@requires_db
def test_rate_limit_applies_to_register(db_engine: Engine):
    """SRS-014에서 준비한 AUTH_RATE_LIMIT이 인증 엔드포인트에 실제로 붙었는지 확인."""
    client = _client(auth_rate_limit="3/minute")
    for index in range(3):
        client.post("/auth/register", json={**VALID, "email": f"user{index}@example.com"})

    response = client.post("/auth/register", json={**VALID, "email": "over@example.com"})

    assert response.status_code == 429
