"""DB 세션 관리. 접속 정보는 환경 변수에서만 읽는다."""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker


def create_db_engine(database_url: str, connect_timeout: int = 5) -> Engine:
    # pool_pre_ping: 오래 놀던 커넥션이 끊겼을 때 조용히 실패하지 않게 한다.
    # connect_timeout: DB가 죽어 있을 때 health 응답이 몇 분씩 매달리지 않게 한다.
    return create_engine(
        database_url,
        pool_pre_ping=True,
        future=True,
        connect_args={"connect_timeout": connect_timeout},
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_session(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    """요청 하나당 세션 하나. 오류가 나면 롤백한다."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def ping(engine: Engine) -> bool:
    """DB가 응답하는지 확인한다(health용)."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
