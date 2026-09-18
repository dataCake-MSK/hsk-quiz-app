from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """서버가 요청을 받을 수 있는지 확인한다. 인증 없이 호출 가능."""
    return HealthResponse(status="ok")
