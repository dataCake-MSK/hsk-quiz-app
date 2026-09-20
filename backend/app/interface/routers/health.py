from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from slowapi import Limiter
from sqlalchemy import Engine

from app.infrastructure.db.session import ping


class HealthResponse(BaseModel):
    status: str
    # "ok" = 연결됨, "unavailable" = 연결 실패, "not_configured" = DATABASE_URL 없음
    db: str


def create_health_router(limiter: Limiter, rate_limit: str, engine: Engine | None) -> APIRouter:
    """rate limit이 앱별 Limiter에 묶이므로 라우터도 앱을 만들 때 생성한다."""
    router = APIRouter(tags=["health"])

    @router.get("/health", response_model=HealthResponse)
    @limiter.limit(rate_limit)
    # request·response 인자는 slowapi가 요구한다(남은 횟수 헤더를 넣기 위해).
    def health(request: Request, response: Response) -> HealthResponse:
        """서버와 DB가 응답하는지 확인한다. 인증 없이 호출 가능."""
        if engine is None:
            return HealthResponse(status="ok", db="not_configured")
        return HealthResponse(status="ok", db="ok" if ping(engine) else "unavailable")

    return router
