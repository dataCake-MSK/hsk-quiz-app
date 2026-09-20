"""요청 횟수 제한(rate limit). slowapi를 쓰고 저장소는 메모리(프로세스 1개 기준)."""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


def build_limiter() -> Limiter:
    """앱마다 새 Limiter를 만든다(테스트끼리 카운터가 섞이지 않게)."""
    return Limiter(key_func=get_remote_address, headers_enabled=True)


async def rate_limit_handler(request: Request, exc: Exception) -> JSONResponse:
    """제한 초과 응답을 프로젝트 오류 형식({"detail": ...})으로 맞춘다."""
    retry_after = getattr(exc, "retry_after", None) if isinstance(exc, RateLimitExceeded) else None
    headers = {"Retry-After": str(retry_after)} if retry_after else None
    return JSONResponse(
        status_code=429,
        content={"detail": "요청이 너무 잦습니다. 잠시 후 다시 시도해 주세요."},
        headers=headers,
    )
