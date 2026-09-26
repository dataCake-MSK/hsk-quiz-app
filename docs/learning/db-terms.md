# DB 용어 사전 (이 프로젝트의 실제 예로)

모두 `words`·`users` 테이블에서 실제로 쓰고 있는 것들이다.

## 1. 대리키 (surrogate key)
**의미 없는 번호를 식별자로 쓰는 것.** DB가 자동으로 1, 2, 3…을 매긴다.

```
word_id | bigint | not null | generated always as identity
```
- 반대는 **자연키**(natural key): 데이터 자체가 가진 고유값. 여기서는 `hanzi`(买).
- 자연키를 PK로 쓰지 않는 이유: 값이 바뀔 수 있고(이메일 변경, 표기 수정), 길고, 다른 테이블에 계속 복사되기 때문.
- "대리"는 진짜 식별자(자연키)를 **대신한다**는 뜻.

## 2. CHECK 제약
**"이 조건을 만족하는 값만 넣을 수 있다"고 DB에 새겨두는 규칙.**

```
ck_words_hsk_level  CHECK (hsk_level >= 1 AND hsk_level <= 3)
ck_users_role       CHECK (role IN ('user', 'admin'))
ck_users_email_lowercase CHECK (email = lower(email))
```
- 애플리케이션 코드에서도 검사하지만, **코드를 우회한 입력**(psql, 다른 프로그램, 내 실수)까지 막으려고 DB에도 건다.
- 위반하면 INSERT/UPDATE 자체가 실패한다.

## 3. nullable FK (값이 비어 있어도 되는 외래키)
**외래키(FK)** = 다른 테이블의 행을 가리키는 컬럼.
**nullable** = 비워 둘 수 있음.

```
owner_id | bigint |  (nullable)
fk_words_owner FOREIGN KEY (owner_id) REFERENCES users(user_id) ON DELETE CASCADE
```
- 이 프로젝트에서 `owner_id`가 **비어 있으면 공용 단어**, **값이 있으면 그 유저의 커스텀 단어**다.
- 즉 "비어 있음"에 **의미를 부여**한 설계다. 공용/개인을 테이블 두 개로 나누지 않고 한 테이블에서 구분한다.
- `ON DELETE CASCADE`: 유저가 삭제되면 그 유저의 커스텀 단어도 함께 사라진다(공용 단어는 영향 없음).

## 4. 부분 유니크 인덱스 (partial unique index)

### 먼저 괄호의 뜻
`UNIQUE (a, b)`에서 괄호 안은 **"이 컬럼들을 묶은 한 세트"**를 뜻한다. a만 유일, b만 유일이 아니라 **(a, b) 조합이 유일**하다는 말이다.

| 쓴 것 | 한국어로 읽으면 |
|---|---|
| `UNIQUE (hanzi)` | 한자 값은 표 전체에서 하나만 있을 수 있다 |
| `UNIQUE (owner_id, hanzi)` | **"주인 + 한자" 조합**이 하나만 있을 수 있다. 주인이 다르면 같은 한자도 괜찮다 |
| `... WHERE owner_id IS NOT NULL` | 위 규칙을 **주인이 있는 행들에만** 적용한다 |

### 우리가 건 두 규칙
```sql
UNIQUE (hanzi)           WHERE owner_id IS NULL      -- ①
UNIQUE (owner_id, hanzi) WHERE owner_id IS NOT NULL  -- ②
```
- ① **"주인이 없는(=공용) 단어들 사이에서는 같은 한자가 두 번 나올 수 없다."**
- ② **"주인이 있는 단어들은, 같은 사람이 같은 한자를 두 번 가질 수 없다."** (다른 사람은 상관없음)

### 실제로 무엇이 허용되고 막히는지
현재 공용 단어 买(word_id 1)가 있는 상태에서:

| 넣으려는 행 | 결과 | 이유 |
|---|---|---|
| owner_id=NULL, hanzi=买 | ❌ 거부 | ①에 걸림 (공용 买가 이미 있음) |
| owner_id=7, hanzi=买 | ✅ 허용 | 7번 유저의 개인 단어. ①은 공용만 보고, ②는 (7, 买)가 처음 |
| owner_id=7, hanzi=买 (또) | ❌ 거부 | ②에 걸림 (같은 사람이 같은 한자 두 번) |
| owner_id=8, hanzi=买 | ✅ 허용 | ②는 (8, 买) 조합을 따로 본다 |

`WHERE` 없이 `UNIQUE (hanzi)` 하나만 걸었다면 두 번째 줄도 막혀서, 유저가 공용에 이미 있는 단어를 자기 방식으로 정리할 수 없게 된다.

## 5. 정션 테이블 (junction table)
**두 테이블의 연결 자체를 담는 테이블.** "연결 테이블", "중간 테이블"이라고도 한다.

예: 단어와 카테고리(#13에서 추가 예정)
```
word_categories
  word_id     ─→ words
  category_id ─→ categories
```
행 하나가 "이 단어에 이 카테고리가 붙어 있다"는 사실 하나를 뜻한다.

## 6. M:N과 정션 — 예시로

### 관계의 세 종류
| 관계 | 읽는 법 | 이 프로젝트 예 |
|---|---|---|
| 1:1 | 하나에 하나 | (아직 없음) |
| 1:N | 하나에 여럿 | 유저 1명 : 그 사람의 커스텀 단어 여러 개 |
| **M:N** | 여럿에 여럿 | 단어 여러 개 ↔ 카테고리 여러 개 |

M:N인지 확인하는 방법은 **양쪽에서 물어보는 것**이다.
- "단어 하나에 카테고리 여러 개 붙나?" → 买는 `쇼핑`이면서 `HSK1 필수`일 수 있다 → 예
- "카테고리 하나에 단어 여러 개 붙나?" → `쇼핑`에는 买, 卖, 钱… → 예
- 양쪽 다 "예"면 **M:N**이다.

### 컬럼으로는 왜 안 되나
```
words
 word_id | hanzi | category
       1 | 买    | 쇼핑          ← 여기에 '여행'도 넣고 싶으면?
```
- `category = '쇼핑,여행'`처럼 넣으면 검색이 문자열 비교가 되고(`'여행'` 찾다가 `'여행사'`도 걸림), 오타를 막을 수 없다.
- 카테고리 이름을 바꾸면 모든 단어 행을 다 고쳐야 한다.

### 정션 테이블로 푸는 법
표 세 개로 나눈다.
```
words                     categories              word_categories (정션)
 word_id | hanzi           category_id | name      word_id | category_id
       1 | 买                        1 | 쇼핑            1 |           1
       2 | 卖                        2 | 여행            1 |           2
       3 | 去                        3 | 이동            2 |           1
                                                        3 |           3
                                                        3 |           2
```
읽는 법:
- 买(1)에는 쇼핑(1)과 여행(2)이 붙어 있다 → **단어 하나에 카테고리 둘**
- 쇼핑(1)에는 买(1)과 卖(2)가 붙어 있다 → **카테고리 하나에 단어 둘**
- 연결 하나가 **행 하나**다. 연결을 지우려면 그 행만 지우면 된다.

### 조회 예
"여행 카테고리 단어 목록"은 정션을 사이에 두고 잇는다.
```sql
SELECT w.hanzi
FROM words w
JOIN word_categories wc ON wc.word_id = w.word_id
JOIN categories c       ON c.category_id = wc.category_id
WHERE c.name = '여행';
-- 买, 去
```
이 표는 #13에서 실제로 만든다.

## 7. 복합 PK (composite primary key)
**기본키를 컬럼 두 개 이상으로 구성하는 것.**

```
word_stats
  PRIMARY KEY (user_id, word_id)
```
- "이 유저의 이 단어에 대한 기록"은 하나뿐이어야 한다 → 두 컬럼을 합쳐야 유일해진다.
- 굳이 `stat_id` 같은 번호를 새로 만들면, 같은 (유저, 단어) 조합이 두 줄 들어가는 것을 막지 못해 UNIQUE를 또 걸어야 한다.
- 정션 테이블에서 자주 쓴다(`word_categories`, `word_bookmarks`, `word_stats`).

## 8. 자기참조 (self-reference) — 예시로

**같은 테이블의 행끼리 연결하는 것.** 보통 FK는 다른 표를 가리키지만, 여기서는 자기 표를 가리킨다.

### 이 프로젝트의 예: 혼동 관계
买도 卖도 둘 다 `words`의 행이다. "이 둘이 헷갈린다"는 사실은 단어 안에 넣을 수 없다(어느 쪽에 넣을 것인가?). 그래서 관계를 담는 표를 따로 만든다.

```
words                          confusion_links (#16에서 생성)
 word_id | hanzi                link_id | word_a_id | word_b_id | confusion_type
       1 | 买                         1 |         1 |         2 | sound     ← 买 vs 卖
       2 | 卖                         2 |         3 |         4 | shape     ← 他 vs 她
       3 | 他                         3 |        11 |        12 | sound     ← 白 vs 百
       4 | 她
      11 | 白
      12 | 百
```
`word_a_id`와 `word_b_id`가 **둘 다 `words.word_id`를 가리킨다.** 이것이 자기참조다.

### 조회 예
"买와 헷갈리는 단어" 찾기 — 같은 표를 두 번 조인한다.
```sql
SELECT b.hanzi, l.confusion_type
FROM confusion_links l
JOIN words a ON a.word_id = l.word_a_id
JOIN words b ON b.word_id = l.word_b_id
WHERE a.hanzi = '买';
-- 卖, sound
```

### 다른 흔한 예
| 상황 | 자기참조 컬럼 |
|---|---|
| 직원과 상사(둘 다 직원) | `employees.manager_id → employees.employee_id` |
| 댓글과 대댓글 | `comments.parent_id → comments.comment_id` |
| 대분류-소분류 | `categories.parent_id → categories.category_id` |

## 9. 쌍 정규화 (pair normalization)
**"A와 B"와 "B와 A"를 같은 것으로 취급하기 위해 저장 순서를 하나로 고정하는 것.**

혼동 관계는 방향이 없다(买가 卖와 헷갈리면 그 반대도 참). 그냥 두면 같은 쌍이 두 줄로 들어갈 수 있다.
```
(1, 2)  -- 买, 卖
(2, 1)  -- 卖, 买   ← 같은 사실인데 다른 행
```
그래서 **항상 작은 번호를 앞에** 두도록 규칙을 정하고 DB에 새긴다.
```
CHECK (word_a_id < word_b_id)
UNIQUE NULLS NOT DISTINCT (word_a_id, word_b_id, added_by)
```
이렇게 하면 `(2, 1)`은 아예 들어가지 못하고, 중복도 UNIQUE가 막는다. 조회할 때도 한 방향만 보면 된다.

## 참고
- PostgreSQL 제약 조건: https://www.postgresql.org/docs/current/ddl-constraints.html
- 부분 인덱스: https://www.postgresql.org/docs/current/indexes-partial.html
- 관련 노트: [데이터 모델링과 식별자(키) 설계](data-modeling-and-keys.md)
