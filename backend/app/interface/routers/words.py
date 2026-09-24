from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from slowapi import Limiter
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.db.models import Word
from app.interface.schemas.word import WordResponse


def create_words_router(
    limiter: Limiter,
    rate_limit: str,
    session_factory: sessionmaker[Session] | None,
) -> APIRouter:
    router = APIRouter(prefix="/words", tags=["words"])

    @router.get("", response_model=list[WordResponse])
    @limiter.limit(rate_limit)
    # request·response 인자는 slowapi가 요구한다.
    def list_words(
        request: Request,
        response: Response,
        hsk_level: int | None = Query(default=None, ge=1, le=3, description="1~3급 필터"),
    ) -> list[WordResponse]:
        """단어 목록.

        TODO(NB-019): 인증을 재개하면 로그인 필수로 바꾸고 조건을
        `owner_id IS NULL OR owner_id = 나`로 넓힌다. 지금은 공용 단어만 돌려준다.
        """
        if session_factory is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="DB가 설정되지 않았습니다.",
            )

        statement = select(Word).where(Word.owner_id.is_(None))
        if hsk_level is not None:
            statement = statement.where(Word.hsk_level == hsk_level)
        statement = statement.order_by(Word.hsk_level, Word.word_id)

        with session_factory() as session:
            words = session.execute(statement).scalars().all()
            return [WordResponse.model_validate(word) for word in words]

    return router
