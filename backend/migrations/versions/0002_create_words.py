"""words 테이블 생성

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-24

owner_id가 NULL이면 공용 단어, 값이 있으면 그 유저의 커스텀 단어(ADR-0004).
부분 유니크 인덱스로 공용/개인 각각의 중복만 막는다.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "words",
        sa.Column("word_id", sa.BigInteger(), sa.Identity(always=True), nullable=False),
        sa.Column("owner_id", sa.BigInteger(), nullable=True),
        sa.Column("hanzi", sa.String(length=20), nullable=False),
        sa.Column("pinyin", sa.String(length=60), nullable=False),
        sa.Column("kr_pronunciation", sa.String(length=60), nullable=False),
        sa.Column("meaning_kr", sa.String(length=200), nullable=False),
        sa.Column("hsk_level", sa.SmallInteger(), nullable=False),
        sa.Column("pos", sa.String(length=20), nullable=True),
        sa.Column("example_sentence", sa.Text(), nullable=True),
        sa.Column("example_meaning_kr", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("word_id", name="pk_words"),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.user_id"], name="fk_words_owner", ondelete="CASCADE"
        ),
        sa.CheckConstraint("hsk_level BETWEEN 1 AND 3", name="ck_words_hsk_level"),
    )
    op.create_index(
        "uq_words_shared_hanzi",
        "words",
        ["hanzi"],
        unique=True,
        postgresql_where=sa.text("owner_id IS NULL"),
    )
    op.create_index(
        "uq_words_owner_hanzi",
        "words",
        ["owner_id", "hanzi"],
        unique=True,
        postgresql_where=sa.text("owner_id IS NOT NULL"),
    )
    op.create_index("ix_words_hsk_level", "words", ["hsk_level"])


def downgrade() -> None:
    op.drop_index("ix_words_hsk_level", table_name="words")
    op.drop_index("uq_words_owner_hanzi", table_name="words")
    op.drop_index("uq_words_shared_hanzi", table_name="words")
    op.drop_table("words")
