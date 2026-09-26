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
**조건을 만족하는 행들 사이에서만 중복을 막는 인덱스.**

```
uq_words_shared_hanzi  UNIQUE (hanzi)             WHERE owner_id IS NULL
uq_words_owner_hanzi   UNIQUE (owner_id, hanzi)   WHERE owner_id IS NOT NULL
```
- 첫 줄: 공용 단어끼리는 같은 한자를 두 번 넣을 수 없다 → **시드를 여러 번 돌려도 안전**.
- 둘째 줄: 한 유저가 같은 한자를 두 번 추가할 수 없다.
- 하지만 **공용에 买가 있어도 유저가 자기 买를 만드는 것은 허용**된다. 일반 UNIQUE 하나로는 이 구분을 표현할 수 없다.

## 5. 정션 테이블 (junction table)
**두 테이블의 연결 자체를 담는 테이블.** "연결 테이블", "중간 테이블"이라고도 한다.

예: 단어와 카테고리(#13에서 추가 예정)
```
word_categories
  word_id     ─→ words
  category_id ─→ categories
```
행 하나가 "이 단어에 이 카테고리가 붙어 있다"는 사실 하나를 뜻한다.

## 6. M:N과 정션
관계는 개수로 나뉜다.

| 관계 | 예 | 표현 방법 |
|---|---|---|
| 1:N (일대다) | 유저 1명 : 커스텀 단어 여러 개 | 단어 쪽에 `owner_id` 컬럼 |
| **M:N (다대다)** | 단어 여러 개 ↔ 카테고리 여러 개 | **정션 테이블이 필요** |

M:N을 컬럼으로 표현할 수 없는 이유:
- `words.category = '여행'` → 태그를 두 개 못 단다.
- `categories.word_ids = '1,2,3'` → 문자열 안에 넣으면 검색·무결성이 다 깨진다.

그래서 **연결을 행으로 저장**한다. 单어 1개에 태그 3개면 정션에 3줄이 생긴다.

## 7. 복합 PK (composite primary key)
**기본키를 컬럼 두 개 이상으로 구성하는 것.**

```
word_stats
  PRIMARY KEY (user_id, word_id)
```
- "이 유저의 이 단어에 대한 기록"은 하나뿐이어야 한다 → 두 컬럼을 합쳐야 유일해진다.
- 굳이 `stat_id` 같은 번호를 새로 만들면, 같은 (유저, 단어) 조합이 두 줄 들어가는 것을 막지 못해 UNIQUE를 또 걸어야 한다.
- 정션 테이블에서 자주 쓴다(`word_categories`, `word_bookmarks`, `word_stats`).

## 8. 자기참조 (self-reference)
**같은 테이블의 행끼리 연결하는 것.**

혼동 관계(#16에서 추가 예정)가 그렇다. 买와 卖는 **둘 다 `words`의 행**이다.
```
confusion_links
  word_a_id ─→ words
  word_b_id ─→ words     ← 같은 테이블을 두 번 참조
```
다른 예: 직원-상사, 댓글-부모 댓글, 카테고리-상위 카테고리.

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
