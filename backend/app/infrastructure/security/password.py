"""비밀번호 해싱. 알고리즘은 Argon2 (ADR-0004, FastAPI 공식 문서 권장).

pwdlib의 `recommended()`는 현재 Argon2id를 쓴다. 나중에 권장값이 바뀌어도
이 모듈만 고치면 되도록 호출부에서는 아래 두 함수만 쓴다.
"""

from __future__ import annotations

from functools import lru_cache

from pwdlib import PasswordHash


@lru_cache(maxsize=1)
def _hasher() -> PasswordHash:
    # 해셔 생성 비용이 있어 한 번만 만든다.
    return PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _hasher().hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _hasher().verify(password, password_hash)
