"""개발용 샘플 단어 20개.

HSK 기준·데이터 출처는 아직 정하지 않았다(NB-016). 구조를 먼저 완성하려고 직접 만든 샘플이며,
기준이 정해지면 이 파일만 교체한다.

고른 기준: **헷갈리기 쉬운 쌍**을 일부러 포함했다(买/卖, 他/她, 左/右, 天/夭 대신 白/百 등).
혼동 관계 자체는 SRS-030에서 `confusion_links`로 따로 넣는다.
"""

from typing import TypedDict


class SampleWord(TypedDict):
    hanzi: str
    pinyin: str
    kr_pronunciation: str
    meaning_kr: str
    hsk_level: int
    pos: str
    example_sentence: str
    example_meaning_kr: str


SAMPLE_WORDS: list[SampleWord] = [
    # --- HSK 1급 ---
    {
        "hanzi": "买",
        "pinyin": "mǎi",
        "kr_pronunciation": "마이",
        "meaning_kr": "사다",
        "hsk_level": 1,
        "pos": "동사",
        "example_sentence": "我想买一本书。",
        "example_meaning_kr": "나는 책 한 권을 사고 싶다.",
    },
    {
        "hanzi": "卖",
        "pinyin": "mài",
        "kr_pronunciation": "마이",
        "meaning_kr": "팔다",
        "hsk_level": 2,
        "pos": "동사",
        "example_sentence": "这里卖水果。",
        "example_meaning_kr": "여기서는 과일을 판다.",
    },
    {
        "hanzi": "他",
        "pinyin": "tā",
        "kr_pronunciation": "타",
        "meaning_kr": "그, 그 사람(남성)",
        "hsk_level": 1,
        "pos": "대명사",
        "example_sentence": "他是我的朋友。",
        "example_meaning_kr": "그는 내 친구다.",
    },
    {
        "hanzi": "她",
        "pinyin": "tā",
        "kr_pronunciation": "타",
        "meaning_kr": "그녀",
        "hsk_level": 1,
        "pos": "대명사",
        "example_sentence": "她在学中文。",
        "example_meaning_kr": "그녀는 중국어를 배우고 있다.",
    },
    {
        "hanzi": "来",
        "pinyin": "lái",
        "kr_pronunciation": "라이",
        "meaning_kr": "오다",
        "hsk_level": 1,
        "pos": "동사",
        "example_sentence": "他明天来我家。",
        "example_meaning_kr": "그는 내일 우리 집에 온다.",
    },
    {
        "hanzi": "去",
        "pinyin": "qù",
        "kr_pronunciation": "취",
        "meaning_kr": "가다",
        "hsk_level": 1,
        "pos": "동사",
        "example_sentence": "我去学校。",
        "example_meaning_kr": "나는 학교에 간다.",
    },
    {
        "hanzi": "大",
        "pinyin": "dà",
        "kr_pronunciation": "따",
        "meaning_kr": "크다",
        "hsk_level": 1,
        "pos": "형용사",
        "example_sentence": "这个房间很大。",
        "example_meaning_kr": "이 방은 매우 크다.",
    },
    {
        "hanzi": "太",
        "pinyin": "tài",
        "kr_pronunciation": "타이",
        "meaning_kr": "너무, 매우",
        "hsk_level": 1,
        "pos": "부사",
        "example_sentence": "今天太热了。",
        "example_meaning_kr": "오늘은 너무 덥다.",
    },
    {
        "hanzi": "上",
        "pinyin": "shàng",
        "kr_pronunciation": "샹",
        "meaning_kr": "위, 오르다",
        "hsk_level": 1,
        "pos": "명사",
        "example_sentence": "书在桌子上。",
        "example_meaning_kr": "책은 책상 위에 있다.",
    },
    {
        "hanzi": "下",
        "pinyin": "xià",
        "kr_pronunciation": "샤",
        "meaning_kr": "아래, 내리다",
        "hsk_level": 1,
        "pos": "명사",
        "example_sentence": "猫在椅子下。",
        "example_meaning_kr": "고양이는 의자 아래에 있다.",
    },
    # --- HSK 2급 ---
    {
        "hanzi": "白",
        "pinyin": "bái",
        "kr_pronunciation": "바이",
        "meaning_kr": "희다, 하얀",
        "hsk_level": 2,
        "pos": "형용사",
        "example_sentence": "她穿白色的衣服。",
        "example_meaning_kr": "그녀는 흰옷을 입는다.",
    },
    {
        "hanzi": "百",
        "pinyin": "bǎi",
        "kr_pronunciation": "바이",
        "meaning_kr": "백(100)",
        "hsk_level": 2,
        "pos": "수사",
        "example_sentence": "这本书一百块钱。",
        "example_meaning_kr": "이 책은 100위안이다.",
    },
    {
        "hanzi": "左",
        "pinyin": "zuǒ",
        "kr_pronunciation": "쭤",
        "meaning_kr": "왼쪽",
        "hsk_level": 2,
        "pos": "명사",
        "example_sentence": "银行在左边。",
        "example_meaning_kr": "은행은 왼쪽에 있다.",
    },
    {
        "hanzi": "右",
        "pinyin": "yòu",
        "kr_pronunciation": "여우",
        "meaning_kr": "오른쪽",
        "hsk_level": 2,
        "pos": "명사",
        "example_sentence": "请往右走。",
        "example_meaning_kr": "오른쪽으로 가세요.",
    },
    {
        "hanzi": "借",
        "pinyin": "jiè",
        "kr_pronunciation": "제",
        "meaning_kr": "빌리다, 빌려주다",
        "hsk_level": 3,
        "pos": "동사",
        "example_sentence": "我想借这本书。",
        "example_meaning_kr": "나는 이 책을 빌리고 싶다.",
    },
    {
        "hanzi": "还",
        "pinyin": "huán",
        "kr_pronunciation": "환",
        "meaning_kr": "돌려주다 (hái로 읽으면 '아직')",
        "hsk_level": 3,
        "pos": "동사",
        "example_sentence": "明天我还你钱。",
        "example_meaning_kr": "내일 네게 돈을 갚을게.",
    },
    # --- HSK 3급 ---
    {
        "hanzi": "简单",
        "pinyin": "jiǎndān",
        "kr_pronunciation": "젠딴",
        "meaning_kr": "간단하다",
        "hsk_level": 3,
        "pos": "형용사",
        "example_sentence": "这个问题很简单。",
        "example_meaning_kr": "이 문제는 아주 간단하다.",
    },
    {
        "hanzi": "简历",
        "pinyin": "jiǎnlì",
        "kr_pronunciation": "젠리",
        "meaning_kr": "이력서",
        "hsk_level": 3,
        "pos": "명사",
        "example_sentence": "请发给我你的简历。",
        "example_meaning_kr": "당신의 이력서를 보내 주세요.",
    },
    {
        "hanzi": "认识",
        "pinyin": "rènshi",
        "kr_pronunciation": "런스",
        "meaning_kr": "(사람을) 알다, 인식하다",
        "hsk_level": 2,
        "pos": "동사",
        "example_sentence": "我认识他的姐姐。",
        "example_meaning_kr": "나는 그의 누나를 안다.",
    },
    {
        "hanzi": "知道",
        "pinyin": "zhīdào",
        "kr_pronunciation": "즈따오",
        "meaning_kr": "(사실을) 알다",
        "hsk_level": 2,
        "pos": "동사",
        "example_sentence": "我知道这件事。",
        "example_meaning_kr": "나는 이 일을 알고 있다.",
    },
]
