from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.infrastructure.config import Settings, load_settings
from app.infrastructure.rate_limit import build_limiter, rate_limit_handler
from app.interface.routers.health import create_health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or load_settings()

    app = FastAPI(title="HSK Quiz API", version="0.1.0")

    limiter = build_limiter()
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

    if settings.cors_origins:
        # 허용 출처는 환경 변수로만 지정한다. 와일드카드(*)는 쓰지 않는다.
        # 토큰은 Authorization 헤더로 보내고 쿠키를 쓰지 않으므로 allow_credentials는 False.
        app.add_middleware(
            CORSMiddleware,
            allow_origins=list(settings.cors_origins),
            allow_credentials=False,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["Authorization", "Content-Type"],
        )

    app.include_router(create_health_router(limiter, settings.public_rate_limit))
    return app


app = create_app()
