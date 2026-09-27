# SQL 조인과 별칭 — 혼동 관계 조회로 익히기

`confusion_links`(자기참조 정션)를 조회하는 쿼리를 한 줄씩 뜯어본다. 실행 결과는 실제 DB에서 뽑은 것이다.

```sql
SELECT b.hanzi, l.confusion_type
FROM confusion_links l
JOIN words a ON a.word_id = l.word_a_id
JOIN words b ON b.word_id = l.word_b_id
WHERE a.hanzi = '买';
```

## 0. 먼저: 쿼리 결과는 테이블이 아니다
psql에 찍히는 표는 **그때 계산해서 만든 결과 묶음**이다. 저장되어 있지 않고 이름도 없다.

| 구분 | 설명 | 예 |
|---|---|---|
| 테이블 | 디스크에 저장되는 실제 표 | `words`, `confusion_links` |
| 쿼리 결과 | 실행할 때만 만들어지는 임시 표 | `SELECT ...`의 출력 |
| 뷰(view) | 쿼리에 이름을 붙여 저장한 것. 볼 때마다 다시 계산 | (이 프로젝트엔 아직 없음) |

`confusion_links`에 **실제로 저장된 내용**은 번호뿐이다.
```
 link_id | word_a_id | word_b_id | confusion_type
---------+-----------+-----------+----------------
       1 |         1 |         2 | sound
       2 |         3 |         4 | shape
       3 |        11 |        12 | sound
```
한자는 여기 없다. `words`에 있다.
```
 word_id | hanzi |    meaning_kr
---------+-------+-------------------
       1 | 买    | 사다
       2 | 卖    | 팔다
       3 | 他    | 그, 그 사람(남성)
       4 | 她    | 그녀
      11 | 白    | 희다, 하얀
      12 | 百    | 백(100)
```
**조인은 이 둘을 붙여서 "번호를 한자로 바꿔 읽는" 작업**이다.

## 1. `FROM confusion_links l` — 별칭 붙이기
표 이름 뒤에 쓴 한 글자가 **별칭(alias)**이다. 이 쿼리 안에서만 `confusion_links`를 `l`이라고 부르겠다는 뜻이다.
`AS`를 써서 `FROM confusion_links AS l`이라고 해도 같다(생략 가능).

별칭은 **쿼리 전체(SELECT·JOIN·WHERE·ORDER BY)에 적용**된다. 그래서 `l.confusion_type`처럼 쓸 수 있다.

## 2. `JOIN words a ON a.word_id = l.word_a_id`
- `words`를 `a`라고 부른다.
- `ON`은 **어떤 행끼리 붙일지**를 정한다. "words의 word_id가 confusion_links의 word_a_id와 같은 행끼리 붙여라."

여기까지만 하면 **왼쪽 단어의 한자만** 알 수 있다.
```
 link_id | a_hanzi | word_b_id
---------+---------+-----------
       1 | 买      |         2     ← 2가 무슨 글자인지는 아직 모름
       2 | 他      |         4
       3 | 白      |        12
```

## 3. `JOIN words b ON b.word_id = l.word_b_id` — 왜 또 하나?
같은 표를 **다른 용도로 한 번 더** 붙이기 위해서다. 한 줄에 단어가 **둘** 들어가야 하는데(왼쪽 단어, 오른쪽 단어), `words`를 한 번만 붙이면 그중 하나밖에 못 가져온다.

- `a` = 왼쪽 단어의 행
- `b` = 오른쪽 단어의 행

둘 다 붙이면 한 줄에 양쪽 한자가 모인다.
```
 link_id | word_a_id | a  | word_b_id | b  | confusion_type
---------+-----------+----+-----------+----+----------------
       1 |         1 | 买 |         2 | 卖 | sound
       2 |         3 | 他 |         4 | 她 | shape
       3 |        11 | 白 |        12 | 百 | sound
```
이 표가 앞서 본 "결과"다. **저장된 테이블이 아니라 조인으로 방금 만든 결과**이며, `a`·`b`는 컬럼 이름이 아니라 `AS a`로 붙인 표시용 이름이다.

### 별칭이 없으면 실제로 오류가 난다
```sql
FROM confusion_links
JOIN words ON ...
JOIN words ON ...   -- ERROR: 테이블 이름 "words"가 한번 이상 명시되어 있습니다
```
PostgreSQL이 "둘 중 어느 words를 말하는지 모르겠다"며 거절한다. 그래서 **같은 표를 두 번 쓸 때 별칭은 선택이 아니라 필수**다.

## 4. `WHERE a.hanzi = '买'`
조인해서 만든 위 표에서 **`a`쪽(왼쪽 단어)이 买인 줄만** 남긴다 → 1번 줄만 남는다.

## 5. `SELECT b.hanzi, l.confusion_type`
남은 줄에서 **보여줄 칸만 고른다.**
- `b.hanzi` = `b`(오른쪽 단어)의 한자 → 卖
- `l.confusion_type` = 혼동 유형 → sound

```
 hanzi | confusion_type
-------+----------------
 卖    | sound
```

## 실행 순서로 다시 정리
SQL은 쓰는 순서와 처리 순서가 다르다.

| 순서 | 절 | 하는 일 |
|---|---|---|
| 1 | `FROM` / `JOIN` | 표를 붙여 넓은 임시 표를 만든다 |
| 2 | `WHERE` | 그중 조건에 맞는 줄만 남긴다 |
| 3 | `SELECT` | 남은 줄에서 보여줄 칸을 고른다 |
| 4 | `ORDER BY` | 정렬한다 |

## 주의점
- 별칭은 **그 쿼리 안에서만** 유효하다. 다른 쿼리에서는 다시 붙여야 한다.
- `a`, `b`, `l` 같은 한 글자는 짧아서 흔하지만, 뜻이 드러나는 이름(`base`, `pair`)이 더 나을 때도 있다.
- `WHERE a.hanzi = '买'`처럼 **조인 뒤 조건**과, `ON a.word_id = ...`처럼 **붙이는 조건**은 역할이 다르다. 헷갈리면 "ON은 붙이는 규칙, WHERE는 거르는 규칙"으로 기억한다.

## 참고
- PostgreSQL 조인: https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN
- 관련 노트: [DB 용어 사전](db-terms.md), [데이터 모델링과 식별자](data-modeling-and-keys.md)
