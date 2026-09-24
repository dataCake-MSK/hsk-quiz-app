from pydantic import BaseModel, ConfigDict


class WordResponse(BaseModel):
    """단어 목록·상세 응답. DB 모델을 그대로 내보내지 않고 필요한 필드만 정한다."""

    model_config = ConfigDict(from_attributes=True)

    word_id: int
    hanzi: str
    pinyin: str
    kr_pronunciation: str
    meaning_kr: str
    hsk_level: int
    pos: str | None
    example_sentence: str | None
    example_meaning_kr: str | None
