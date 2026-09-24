"""SQLAlchemy 모델. 도메인 엔티티와는 분리한다(ADR-0003).

제약은 되도록 DB에도 건다. 애플리케이션 코드를 우회해 들어오는 값까지 막기 위해서다.
"""

from __future__ import annotations

import datetime as dt

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    SmallInteger,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

ROLE_USER = "user"
ROLE_ADMIN = "admin"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(f"role IN ('{ROLE_USER}', '{ROLE_ADMIN}')", name="ck_users_role"),
        CheckConstraint("email = lower(email)", name="ck_users_email_lowercase"),
    )

    user_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    # 대소문자만 다른 중복 가입을 막기 위해 소문자로만 저장한다(CHECK로 강제).
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False, server_default=ROLE_USER)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class Word(Base):
    """단어. owner_id가 NULL이면 모두가 함께 쓰는 공용 단어, 값이 있으면 그 유저의 커스텀 단어."""

    __tablename__ = "words"
    __table_args__ = (
        CheckConstraint("hsk_level BETWEEN 1 AND 3", name="ck_words_hsk_level"),
        # 공용 단어끼리는 한자가 겹치지 않게 한다(시드를 여러 번 돌려도 늘어나지 않도록).
        Index(
            "uq_words_shared_hanzi",
            "hanzi",
            unique=True,
            postgresql_where=text("owner_id IS NULL"),
        ),
        # 한 유저가 같은 한자를 두 번 추가하는 것도 막는다.
        Index(
            "uq_words_owner_hanzi",
            "owner_id",
            "hanzi",
            unique=True,
            postgresql_where=text("owner_id IS NOT NULL"),
        ),
        Index("ix_words_hsk_level", "hsk_level"),
    )

    word_id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    owner_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True
    )
    hanzi: Mapped[str] = mapped_column(String(20), nullable=False)
    pinyin: Mapped[str] = mapped_column(String(60), nullable=False)
    kr_pronunciation: Mapped[str] = mapped_column(String(60), nullable=False)
    meaning_kr: Mapped[str] = mapped_column(String(200), nullable=False)
    hsk_level: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    pos: Mapped[str | None] = mapped_column(String(20), nullable=True)
    example_sentence: Mapped[str | None] = mapped_column(Text, nullable=True)
    example_meaning_kr: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
