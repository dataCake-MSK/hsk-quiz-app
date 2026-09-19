# 남의 리소스 접근은 403이 아니라 404로 응답하기

## 핵심 개념
| 코드 | 뜻 | 응답이 알려주는 것 |
|---|---|---|
| 401 Unauthorized | 누구인지 모름(토큰 없음·만료·위조) | "로그인하세요" |
| 403 Forbidden | 누구인지는 알지만 이 일을 할 권한이 없음 | "그건 있지만 당신은 못 합니다" → **대상이 존재한다는 사실이 새어 나감** |
| 404 Not Found | 대상이 없음 | "그런 건 없습니다" |

- 유저 A가 `GET /quiz/sessions/102`를 보냈는데 102가 유저 B의 세션이라면:
  - 403을 주면 A는 "102번 세션은 존재한다"는 것을 알게 된다. 번호를 1, 2, 3… 바꿔 보며 **다른 유저의 데이터가 있는지 탐색**할 수 있다(IDOR 공격의 사전 조사).
  - 404를 주면 "없는 세션"과 "남의 세션"이 구분되지 않는다. A 입장에서 **B의 데이터는 처음부터 존재하지 않는 것**과 같다.
- 구현도 자연스럽다: 조회할 때부터 `WHERE session_id = :id AND user_id = :me`로 찾으면 남의 것은 결과가 비어서 404가 된다. "먼저 찾고 → 소유자를 비교해 403"보다 **빠뜨리기 어려운 방식**이다.

## 이 프로젝트 적용
- [ADR-0004](../architecture/adr/0004-auth-and-identifiers.md), [arc42 8.3](../architecture/arc42.md#83-오류-응답)
  - 유저 소유 리소스(세션, 즐겨찾기, 숙련도, 커스텀 단어)에 남이 접근 → **404**
  - 역할이 부족한 경우(일반 유저가 공용 단어에 카테고리 태그) → **403**. 공용 단어는 원래 모두에게 보이므로 존재를 숨길 이유가 없다
- 모든 유저 소유 API에 "다른 유저 토큰으로 요청 → 404" 테스트를 둔다(SRS 공통 AC).
- SRS-025(Repository 도입)부터는 조회 메서드가 `user_id`를 필수 인자로 받아, 필터를 빼먹는 실수를 구조적으로 막는다.

## 삽질 / 주의점
- 403과 404를 섞어 쓰면 오히려 정보가 샌다. "유저 소유 리소스는 항상 404"처럼 규칙을 하나로 정해 둔다.
- 404로 숨겨도 **인가 검사를 대신하지는 않는다.** 필터가 빠지면 남의 데이터가 그대로 200으로 나간다. 테스트가 중요하다.

## 참고
- OWASP API Security Top 10 — API1:2023 Broken Object Level Authorization: https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization
- RFC 9110 15.5.4 403 Forbidden — "An origin server that wishes to "hide" the current existence of a forbidden target resource MAY instead respond with a status code of 404 (Not Found).": https://www.rfc-editor.org/rfc/rfc9110#name-403-forbidden
