"""SQLAlchemy 모델. 도메인 엔티티와는 분리한다(ADR-0003).

제약은 되도록 DB에도 건다. 애플리케이션 코드를 우회해 들어오는 값까지 막기 위해서다.
"""

from __future__ import annotations

import datetime as dt

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Identity, String, func
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
