"""공용 데이터 시드 CLI.

    uv run --env-file .env python -m app.infrastructure.seed words

여러 번 실행해도 결과가 같아야 한다(중복 삽입 없음).
"""

from __future__ import annotations

import sys

from sqlalchemy import func, select

from app.infrastructure.config import load_settings
from app.infrastructure.db.models import Word
from app.infrastructure.db.session import create_db_engine, create_session_factory
from app.infrastructure.seed.words_data import SAMPLE_WORDS


def _use_utf8_output() -> None:
    """한국어 Windows 콘솔은 기본이 cp949라 한글 출력에서 UnicodeEncodeError가 난다."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def seed_words() -> tuple[int, int]:
    """공용 단어를 넣는다. (새로 넣은 수, 이미 있어 건너뛴 수)를 돌려준다."""
    settings = load_settings()
    if not settings.database_url:
        raise SystemExit("DATABASE_URL이 없습니다. `uv run --env-file .env ...`로 실행하세요.")

    engine = create_db_engine(settings.database_url)
    session_factory = create_session_factory(engine)

    inserted = 0
    skipped = 0
    with session_factory() as session:
        existing = set(
            session.execute(select(Word.hanzi).where(Word.owner_id.is_(None))).scalars().all()
        )
        for row in SAMPLE_WORDS:
            if row["hanzi"] in existing:
                skipped += 1
                continue
            session.add(Word(owner_id=None, **row))
            inserted += 1
        session.commit()

        total = session.execute(
            select(func.count()).select_from(Word).where(Word.owner_id.is_(None))
        ).scalar_one()

    engine.dispose()
    print(f"공용 단어 시드 완료: 추가 {inserted}개, 건너뜀 {skipped}개, 현재 총 {total}개")
    return inserted, skipped


def main(argv: list[str]) -> int:
    _use_utf8_output()
    if len(argv) != 1 or argv[0] != "words":
        print("사용법: python -m app.infrastructure.seed words", file=sys.stderr)
        return 2
    seed_words()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
