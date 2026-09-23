from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    # 8자 미만은 거부한다(SRS-010). 상한은 Argon2 처리 비용을 막기 위한 안전장치.
    password: str = Field(min_length=8, max_length=128)
    nickname: str = Field(min_length=1, max_length=50)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        """대소문자만 다른 중복 가입을 막기 위해 소문자로 저장한다(DB에도 CHECK가 있다)."""
        return value.strip().lower()

    @field_validator("nickname")
    @classmethod
    def strip_nickname(cls, value: str) -> str:
        return value.strip()


class UserResponse(BaseModel):
    """응답에는 비밀번호 해시를 절대 넣지 않는다."""

    user_id: int
    email: str
    nickname: str
