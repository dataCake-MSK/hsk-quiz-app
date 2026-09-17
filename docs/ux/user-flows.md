# User Flow — HSK Quiz App (MVP)

- 버전: v0 (2026-09-17). 화면 이름(login, word-list 등)은 [wireframes/](wireframes/)의 제목과 같다.

## 전체 흐름

```mermaid
flowchart TD
  start([앱 실행]) --> hasToken{저장된 토큰 있음?}
  hasToken -- 아니오 --> login[로그인]
  hasToken -- 예 --> me{GET /users/me 성공?}
  me -- 401, refresh 실패 --> login
  me -- 성공 --> home[홈]
  login -- 계정 없음 --> register[회원가입]
  register -- 201 --> login
  login -- 200 토큰 저장 --> home

  home --> words[단어 목록]
  home --> quizStart[퀴즈 시작]
  home -- 로그아웃 --> login

  words -- 급수·카테고리·즐겨찾기 필터 --> words
  words -- 단어 선택 --> detail[단어 상세]
  words -- + 버튼 --> addWord[커스텀 단어 추가]
  addWord -- 저장 --> words
  detail -- ☆/★ 토글 --> detail

  words -- 즐겨찾기 탭에서 퀴즈 --> quizStart
  quizStart -- POST /quiz/sessions --> quiz[퀴즈 문제]
  quiz -- 보기 선택, POST answer --> feedback[정답/오답 표시]
  feedback -- 10문제 미만 --> quiz
  feedback -- 10문제 완료, POST complete --> result[결과]
  result -- 다시 풀기 --> quizStart
  result -- 홈으로 --> home
```

## 퀴즈 1문제의 흐름 (앱 ↔ API)

```mermaid
sequenceDiagram
  actor U as 학습자
  participant M as Mobile App
  participant A as API
  participant D as DB
  U->>M: 퀴즈 시작
  M->>A: POST /quiz/sessions {mode: normal}
  A->>D: quiz_sessions INSERT (user_id = 나)
  A-->>M: 201 {session_id}
  M->>A: GET /quiz/sessions/{id}/next-question
  A->>D: 낮은 mastery 단어 + 그 단어의 혼동 단어 조회
  A-->>M: 문제 + 보기 4개 (정답 표시 없음)
  U->>M: 보기 선택
  M->>A: POST /quiz/sessions/{id}/answer
  A->>D: quiz_questions 갱신, word_stats UPSERT
  A-->>M: {is_correct, answer_word_id}
  M-->>U: 정답/오답 표시 → 다음 문제
```

## 시나리오별 확인 경로
| 시나리오 | 화면 순서 | SRS |
|---|---|---|
| 가입·로그인 | login → register → login → home | SRS-013 |
| 단어 보기 | home → word-list(급수 탭) → word-detail | SRS-021 |
| 커스텀 단어 | word-list → 추가 → word-list | SRS-022 |
| 즐겨찾기 | word-detail ☆ → word-list 즐겨찾기 탭 | SRS-024 |
| 일반 퀴즈 | home → quiz ×10 → result | SRS-030~033 |
| 즐겨찾기 퀴즈 | word-list 즐겨찾기 탭 → quiz → result | SRS-034 |
