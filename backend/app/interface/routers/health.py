from fastapi import APIRouter, Request, Response
from pydantic import BaseModel
from slowapi import Limiter


class HealthResponse(BaseModel):
    status: str


def create_health_router(limiter: Limiter, rate_limit: str) -> APIRouter:
    """rate limit이 앱별 Limiter에 묶이므로 라우터도 앱을 만들 때 생성한다."""
    router = APIRouter(tags=["health"])

    @router.get("/health", response_model=HealthResponse)
    @limiter.limit(rate_limit)
    # request·response 인자는 slowapi가 요구한다(남은 횟수 헤더를 넣기 위해).
    def health(request: Request, response: Response) -> HealthResponse:
        """서버가 요청을 받을 수 있는지 확인한다. 인증 없이 호출 가능."""
        return HealthResponse(status="ok")

    return router
