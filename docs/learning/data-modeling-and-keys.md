# 데이터 모델링과 식별자(키) 설계

## 핵심 개념

### 1. 식별자는 두 종류다
| 종류 | 뜻 | 이 프로젝트 예 |
|---|---|---|
| **대리키(surrogate key)** | 의미 없는 번호. DB가 채번한다 | `word_id`, `user_id` |
| **자연키(natural key)** | 데이터 자체가 가진 고유값 | 단어의 `hanzi`, 유저의 `email` |

둘 다 쓰는 것이 보통이다. **대리키를 PK로 두고(조인·FK용), 자연키에는 UNIQUE 제약을 건다(중복 방지용).**

왜 자연키를 PK로 안 쓰나:
- 자연키는 **바뀔 수 있다.** 이메일은 바꿀 수 있고, 한자도 표기 수정이 생길 수 있다. PK가 바뀌면 그 값을 참조하는 모든 행을 같이 고쳐야 한다.
- 자연키는 **길다.** `hanzi`를 FK로 쓰면 `word_stats`, `question_choices` 등 여러 테이블에 문자열이 중복 저장된다.
- 여러 컬럼이 합쳐져야 유일해지는 경우가 많다.

### 2. 정션 테이블은 복합 PK가 자연스럽다
`word_stats`처럼 "누가 어떤 단어를 얼마나 아는가"를 담는 표는 `(user_id, word_id)` 자체가 유일하다. 여기에 굳이 `stat_id`를 새로 만들면
- 같은 (user, word) 조합이 두 줄 들어가는 것을 막지 못한다(따로 UNIQUE를 또 걸어야 함)
- 조회는 항상 (user_id, word_id)로 하는데 PK 인덱스를 못 쓴다

그래서 **정션은 복합 PK, 독립 엔터티는 단일 대리키**가 기본이다.

### 3. 자동 채번 번호는 환경마다 다르다
`word_id = 1`이 내 PC에서는 买지만, 다른 DB에서는 다른 단어일 수 있다. 그래서
- **시드 데이터끼리 서로를 참조할 때는 번호가 아니라 자연키로 찾아야 한다.** 예: 혼동 관계 시드는 "1번과 2번"이 아니라 "买와 卖"로 적고, 넣을 때 한자로 `word_id`를 조회한다(SRS-030에서 이렇게 한다).
- 외부 데이터(공식 HSK 목록 등)를 가져오면 그쪽 식별자를 보관할 컬럼(`source`, `source_ref`)이 필요해질 수 있다. 지금은 출처가 정해지지 않아(NB-016) 만들지 않는다.

## 이 프로젝트 적용

### 현재 테이블의 키
| 테이블 | PK | 자연키(UNIQUE) |
|---|---|---|
| `users` | `user_id` (BIGINT identity) | `email` |
| `words` | `word_id` (BIGINT identity) | `hanzi` — **부분 유니크**: 공용은 `WHERE owner_id IS NULL`, 개인은 `(owner_id, hanzi)` |

부분 유니크 인덱스를 쓴 이유: "공용 단어끼리는 한자 중복 금지, 하지만 유저가 같은 한자를 자기 커스텀 단어로 갖는 것은 허용"을 한 번에 표현할 수 있다.

### 앞으로 만들 테이블의 키 (점검 결과)
| 테이블 | PK | 판단 |
|---|---|---|
| `categories` | `category_id` | 독립 엔터티 → 대리키. `name`에 UNIQUE |
| `word_categories` | (`word_id`, `category_id`) | 정션 → 복합 PK |
| `word_bookmarks` | (`user_id`, `word_id`) | 정션 → 복합 PK |
| `word_stats` | (`user_id`, `word_id`) | 정션 → 복합 PK |
| `confusion_links` | `link_id` | 같은 쌍을 여러 사람이 각각 등록할 수 있어 대리키 + `UNIQUE(word_a, word_b, added_by)` |
| `quiz_sessions` | `session_id` | 독립 엔터티 |
| `quiz_questions` | `question_id` | 독립 엔터티 |
| `question_choices` | `choice_id` | 독립 엔터티(같은 문제에 같은 단어가 두 번 들어가지 않도록 UNIQUE(question_id, word_id) 추가 예정) |

**결론: 식별자가 빠진 테이블은 없다.** 정션 3개는 복합 PK가 더 알맞아 단일 번호를 두지 않는다.

### 왜 단어에 카테고리 컬럼을 넣지 않나 (정규화)
`words.category = '여행'` 식으로 넣으면
- 한 단어에 태그를 두 개 이상 달 수 없다
- 오타가 섞인다("여행", "여행 ", "Travel")
- "여행 태그가 붙은 단어 목록"을 찾기 어려워진다

그래서 카테고리를 별도 테이블로 빼고 `word_categories` 정션으로 잇는다. 이것이 **1:N / M:N을 구분해 테이블을 나누는** 기본 규칙이다.

## 진행 계획과 데이터 모델링의 관계

데이터 모델링은 보통 세 단계로 설명한다. 우리 계획은 이 순서를 그대로 따라간다.

| 단계 | 하는 일 | 이 프로젝트에서 |
|---|---|---|
| **개념 모델** | 무엇이 있고 무엇과 무엇이 관계되는가 | 기획 메모의 ERD(arc42 5.3) — 유저·단어·혼동·세션 |
| **논리 모델** | 속성·키·제약을 정한다 | SRS의 각 항목이 테이블 정의를 포함 |
| **물리 모델** | 실제 DB에 만든다 | 마이그레이션 파일(`0001`, `0002`…) |

그리고 기능 순서가 곧 **모델을 아래에서 위로 쌓는 순서**다.

| 이슈 | 새로 만드는 것 | 모델링에서 배우는 것 |
|---|---|---|
| #4 `users` | 기준 엔터티 | 대리키, CHECK 제약, timestamptz |
| #10 `words` | 마스터 데이터 | nullable FK로 공용/개인 구분, 부분 유니크 |
| #13 `categories`·`word_categories` | 분류 | M:N과 정션, 복합 PK |
| #16 `confusion_links` | 관계 그 자체 | **자기참조**(단어↔단어), 쌍 정규화(`a < b` CHECK) |
| #17 `word_stats` 등 | 사람×단어 | 유저별 분리, 간접 소유(세션 경유) |

즉 "기능을 하나씩 만든다"와 "모델을 한 조각씩 완성한다"가 같은 일이다. 새 테이블을 넣을 때마다 **키를 무엇으로 할지, 제약을 어디에 걸지**를 한 번씩 결정하게 되는 것이 이 프로젝트의 학습 목표 ①에 해당한다.

## 삽질 / 주의점
- PK가 있다고 중복이 막히는 것은 아니다. `word_id`가 있어도 같은 한자를 두 번 넣을 수 있다 → **자연키 UNIQUE를 따로 걸어야** 한다(실제로 시드 멱등성이 여기에 달려 있다).
- 마이그레이션 번호(`0001`, `0002`)는 **적용 순서**를 뜻할 뿐 데이터 식별자가 아니다.
- 시드 파일에 `word_id`를 직접 적지 않는다. 환경마다 번호가 달라지기 때문이다.

## 참고
- PostgreSQL identity 컬럼: https://www.postgresql.org/docs/current/ddl-identity-columns.html
- 부분 인덱스(partial index): https://www.postgresql.org/docs/current/indexes-partial.html
- 관련 문서: [ADR-0004 인증·인가·식별자](../architecture/adr/0004-auth-and-identifiers.md), [arc42 5.3 ERD](../architecture/arc42.md#53-데이터-모델-원안--보강)
