"""환경 변수에서 읽는 설정. 비밀 값은 코드에 두지 않고 .env에서만 읽는다."""

from __future__ import annotations

import os
from dataclasses import dataclass

# 공개 엔드포인트(/health 등) 기본 제한. 앱이 주기적으로 호출하므로 인증보다 넉넉하게 둔다.
DEFAULT_PUBLIC_RATE_LIMIT = "30/minute"
# 로그인·회원가입 기본 제한. SRS-010·011에서 해당 라우터에 적용한다.
DEFAULT_AUTH_RATE_LIMIT = "5/minute"


@dataclass(frozen=True)
class Settings:
    cors_origins: tuple[str, ...]
    public_rate_limit: str
    auth_rate_limit: str
    # 형식: postgresql+psycopg://<사용자>:<비밀번호>@<호스트>:<포트>/<DB>
    # 값은 .env에만 두고 저장소에는 넣지 않는다. 없으면 DB 기능 없이 뜬다(health가 알려준다).
    database_url: str | None = None


def _parse_origins(raw: str | None) -> tuple[str, ...]:
    """CORS_ORIGINS="http://a,https://b" → ("http://a", "https://b")."""
    if not raw:
        return ()
    return tuple(origin.strip() for origin in raw.split(",") if origin.strip())


def load_settings() -> Settings:
    return Settings(
        cors_origins=_parse_origins(os.getenv("CORS_ORIGINS")),
        public_rate_limit=os.getenv("PUBLIC_RATE_LIMIT", DEFAULT_PUBLIC_RATE_LIMIT),
        auth_rate_limit=os.getenv("AUTH_RATE_LIMIT", DEFAULT_AUTH_RATE_LIMIT),
        database_url=os.getenv("DATABASE_URL") or None,
    )
