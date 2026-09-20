"""users 테이블의 제약이 DB에서 실제로 동작하는지 확인한다 (SRS-004)."""

from __future__ import annotations

import pytest
from sqlalchemy import Engine, inspect, text
from sqlalchemy.exc import IntegrityError

from tests.conftest import requires_db

VALID = {
    "email": "a@example.com",
    "password_hash": "$argon2id$dummy",
    "nickname": "민트",
}


def _insert(engine: Engine, **overrides: object) -> None:
    row = {**VALID, **overrides}
    columns = ", ".join(row)
    values = ", ".join(f":{key}" for key in row)
    with engine.begin() as connection:
        connection.execute(text(f"INSERT INTO users ({columns}) VALUES ({values})"), row)


@requires_db
def test_table_has_expected_columns(db_engine: Engine):
    columns = {c["name"]: c for c in inspect(db_engine).get_columns("users")}

    assert set(columns) == {
        "user_id",
        "email",
        "password_hash",
        "nickname",
        "role",
        "created_at",
    }
    assert columns["created_at"]["type"].timezone is True


@requires_db
def test_role_defaults_to_user(db_engine: Engine):
    _insert(db_engine)

    with db_engine.connect() as connection:
        role = connection.execute(text("SELECT role FROM users")).scalar_one()

    assert role == "user"


@requires_db
def test_duplicate_email_is_rejected(db_engine: Engine):
    _insert(db_engine)

    with pytest.raises(IntegrityError):
        _insert(db_engine)


@requires_db
def test_uppercase_email_is_rejected(db_engine: Engine):
    """대소문자만 다른 중복 가입을 막기 위해 소문자만 저장한다."""
    with pytest.raises(IntegrityError):
        _insert(db_engine, email="A@example.com")


@requires_db
def test_unknown_role_is_rejected(db_engine: Engine):
    with pytest.raises(IntegrityError):
        _insert(db_engine, role="superadmin")


@requires_db
def test_user_id_is_generated_by_db(db_engine: Engine):
    _insert(db_engine)
    _insert(db_engine, email="b@example.com")

    with db_engine.connect() as connection:
        ids = connection.execute(text("SELECT user_id FROM users ORDER BY user_id")).scalars().all()

    assert ids == [1, 2]
