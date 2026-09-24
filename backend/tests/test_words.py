"""단어 테이블·시드·목록 API (SRS-020)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.infrastructure.config import Settings
from app.infrastructure.db.models import User, Word
from app.infrastructure.seed.words_data import SAMPLE_WORDS
from app.main import create_app
from tests.conftest import TEST_DATABASE_URL, requires_db


def _client() -> TestClient:
    settings = Settings(
        cors_origins=(),
        public_rate_limit="200/minute",
        auth_rate_limit="5/minute",
        database_url=TEST_DATABASE_URL,
    )
    return TestClient(create_app(settings))


def _seed(engine: Engine) -> None:
    """CLI와 같은 규칙(이미 있는 한자는 건너뜀)으로 공용 단어를 넣는다."""
    with Session(engine) as session:
        existing = set(
            session.execute(select(Word.hanzi).where(Word.owner_id.is_(None))).scalars().all()
        )
        for row in SAMPLE_WORDS:
            if row["hanzi"] not in existing:
                session.add(Word(owner_id=None, **row))
        session.commit()


def _count(engine: Engine) -> int:
    with Session(engine) as session:
        return session.execute(select(func.count()).select_from(Word)).scalar_one()


@requires_db
def test_seed_is_idempotent(db_engine: Engine):
    _seed(db_engine)
    first = _count(db_engine)

    _seed(db_engine)

    assert first == len(SAMPLE_WORDS)
    assert _count(db_engine) == first


@requires_db
def test_duplicate_shared_hanzi_is_rejected(db_engine: Engine):
    _seed(db_engine)

    with Session(db_engine) as session, pytest.raises(IntegrityError):
        session.add(Word(owner_id=None, **SAMPLE_WORDS[0]))
        session.commit()


@requires_db
def test_hsk_level_out_of_range_is_rejected(db_engine: Engine):
    with Session(db_engine) as session, pytest.raises(IntegrityError):
        session.add(Word(**{**SAMPLE_WORDS[0], "hsk_level": 5}, owner_id=None))
        session.commit()


@requires_db
def test_list_words_returns_all_shared_words(db_engine: Engine):
    _seed(db_engine)

    response = _client().get("/words")

    assert response.status_code == 200
    assert len(response.json()) == len(SAMPLE_WORDS)


@requires_db
def test_list_words_filters_by_hsk_level(db_engine: Engine):
    _seed(db_engine)
    expected = sum(1 for word in SAMPLE_WORDS if word["hsk_level"] == 1)

    body = _client().get("/words", params={"hsk_level": 1}).json()

    assert len(body) == expected
    assert {word["hsk_level"] for word in body} == {1}


@requires_db
def test_response_fields_match_schema(db_engine: Engine):
    _seed(db_engine)

    word = _client().get("/words", params={"hsk_level": 1}).json()[0]

    assert set(word) == {
        "word_id",
        "hanzi",
        "pinyin",
        "kr_pronunciation",
        "meaning_kr",
        "hsk_level",
        "pos",
        "example_sentence",
        "example_meaning_kr",
    }
    # owner_id 같은 내부 값은 노출하지 않는다.
    assert "owner_id" not in word


@requires_db
def test_invalid_hsk_level_returns_422(db_engine: Engine):
    assert _client().get("/words", params={"hsk_level": 9}).status_code == 422


@requires_db
def test_word_owned_by_a_user_is_not_listed(db_engine: Engine):
    """소유자가 있는 단어(커스텀 단어)는 공용 목록에 섞이지 않는다."""
    _seed(db_engine)
    with Session(db_engine) as session:
        user = User(
            email="owner@example.com",
            password_hash="$argon2id$dummy",
            nickname="주인",
        )
        session.add(user)
        session.flush()
        session.add(
            Word(
                owner_id=user.user_id,
                hanzi="私有",
                pinyin="sīyǒu",
                kr_pronunciation="쓰여우",
                meaning_kr="개인 소유",
                hsk_level=3,
                pos="명사",
                example_sentence=None,
                example_meaning_kr=None,
            )
        )
        session.commit()

    body = _client().get("/words").json()

    assert len(body) == len(SAMPLE_WORDS)
    assert all(word["hanzi"] != "私有" for word in body)
