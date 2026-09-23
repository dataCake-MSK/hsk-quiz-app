from fastapi import APIRouter, HTTPException, Request, Response, status
from slowapi import Limiter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from app.infrastructure.db.models import User
from app.infrastructure.security.password import hash_password
from app.interface.schemas.auth import RegisterRequest, UserResponse


def create_auth_router(
    limiter: Limiter,
    rate_limit: str,
    session_factory: sessionmaker[Session] | None,
) -> APIRouter:
    """인증 라우터. rate limit이 앱별 Limiter에 묶여 있어 앱을 만들 때 생성한다."""
    router = APIRouter(prefix="/auth", tags=["auth"])

    @router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
    # 무차별 대입·대량 가입을 늦추기 위한 IP 기준 제한 (SRS-014에서 준비한 AUTH_RATE_LIMIT).
    @limiter.limit(rate_limit)
    def register(request: Request, response: Response, payload: RegisterRequest) -> UserResponse:
        if session_factory is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="DB가 설정되지 않았습니다.",
            )

        user = User(
            email=payload.email,
            password_hash=hash_password(payload.password),
            nickname=payload.nickname,
        )

        with session_factory() as session:
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                # UNIQUE(email) 위반. 이메일은 스키마에서 이미 소문자로 정규화했다.
                session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="이미 가입된 이메일입니다.",
                ) from None
            session.refresh(user)

            return UserResponse(
                user_id=user.user_id,
                email=user.email,
                nickname=user.nickname,
            )

    return router
