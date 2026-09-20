"""테스트 공용 설정.

DB가 필요한 테스트는 `TEST_DATABASE_URL`이 있을 때만 돈다.
로컬에 DB가 없어도 나머지 테스트는 그대로 통과해야 하기 때문이다(CI에서는 항상 돈다).
"""

from __future__ import annotations

import os

import pytest
from sqlalchemy import Engine, text

from app.infrastructure.db.models import Base
from app.infrastructure.db.session import create_db_engine

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

requires_db = pytest.mark.skipif(
    not TEST_DATABASE_URL, reason="TEST_DATABASE_URL이 없어 DB 테스트를 건너뜁니다"
)


@pytest.fixture(scope="session")
def db_engine() -> Engine:
    if not TEST_DATABASE_URL:
        pytest.skip("TEST_DATABASE_URL 없음")
    engine = create_db_engine(TEST_DATABASE_URL)
    # 테스트는 마이그레이션이 아니라 모델 정의로 스키마를 만든다(빠르고 독립적).
    # 마이그레이션 자체는 CI의 alembic 단계에서 따로 검증한다.
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(autouse=True)
def clean_users(request: pytest.FixtureRequest):
    """DB를 쓰는 테스트마다 users를 비운다."""
    if "db_engine" not in request.fixturenames:
        yield
        return
    engine: Engine = request.getfixturevalue("db_engine")
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    yield
