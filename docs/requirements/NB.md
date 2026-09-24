# NB — Needs Backlog (니즈 덤프)

형식에 구애받지 않고 니즈를 모으는 곳입니다. 다듬어진 항목은 PRD로 승격합니다.

- 상태: `new`(새로 들어옴) · `promoted`(PRD로 승격) · `hold`(보류) · `dropped`(버림)
- 출처 "기획 메모"는 2026-09-17 프로젝트 부트스트랩 요청에 들어 있던 내용입니다.

| ID | 니즈 | 출처 | 등록일 | 상태 | 승격 |
|---|---|---|---|---|---|
| NB-001 | 랜덤 출제가 아니라 **헷갈리는 단어를 추적해 그 조합 위주로 출제**하고 싶다. 사전에 정의된 혼동 관계와 퀴즈 중 직접 태깅한 혼동 관계를 함께 쓴다 | 기획 메모 | 2026-09-17 | promoted | → PRD-005, PRD-006 |
| NB-002 | 이메일+비밀번호로 가입·로그인하고, 이후 요청은 모두 토큰으로 인증하고 싶다 | 기획 메모 | 2026-09-17 | promoted | → PRD-001 |
| NB-003 | HSK 1~3급 단어를 한꺼번에 등록하고, 필요하면 커스텀 단어를 추가하고 싶다 | 기획 메모 | 2026-09-17 | promoted | → PRD-002 |
| NB-004 | 단어에 카테고리(운동/취미/여행 등) 태그, 예문, 한국어 발음 표기를 붙여 보고 싶다 | 기획 메모 | 2026-09-17 | promoted | → PRD-003 |
| NB-005 | 단어를 즐겨찾기하고, 즐겨찾기만 모아 보거나 즐겨찾기 단어로 퀴즈를 풀고 싶다 | 기획 메모 | 2026-09-17 | promoted | → PRD-004 |
| NB-006 | 퀴즈 중 틀리면 "이 단어랑 헷갈렸어요"를 골라 혼동 관계를 직접 추가하고, 다음 문제부터 반영되면 좋겠다 | 기획 메모 | 2026-09-17 | promoted | → PRD-006 (2차) |
| NB-007 | 최근 세션의 오답만 모아 다시 풀고 싶다 (오답노트/재도전) | 기획 메모 | 2026-09-17 | promoted | → PRD-007 (2차) |
| NB-008 | 취약 단어 목록과 HSK 급수별 숙련도를 통계로 보고 싶다 | 기획 메모 | 2026-09-17 | promoted | → PRD-008 (2차) |
| NB-009 | 문제마다 제한시간이 있는 타임어택 모드로 응답 속도도 기록하고 싶다 | 기획 메모 | 2026-09-17 | promoted | → PRD-009 (3차) |
| NB-010 | 목숨·콤보·점수·중간보스 2개가 있는 텍스트 기반 던전 모드로 게임처럼 풀고 싶다 (층 개념 없음, 그림 없음) | 기획 메모 | 2026-09-17 | promoted | → PRD-010 (3차) |
| NB-011 | 이 프로젝트로 **DB 설계**(식별자 체계, 외래키, 자기참조·M:N 정션 테이블, 유저별 데이터 분리)를 배우고 싶다 | 기획 메모 | 2026-09-17 | promoted | → PRD 학습 목표 |
| NB-012 | **클린 아키텍처 4계층**과 Repository/Strategy/Factory 패턴을 배우고 싶다. 단, 패턴은 필요해진 시점에 리팩토링으로 하나씩 도입하고 이유를 ADR로 남긴다 | 기획 메모 | 2026-09-17 | promoted | → PRD 학습 목표, ADR-0003 |
| NB-013 | 배포에 대비한 **최소 보안**(인증·인가, 데이터 접근 제어, 비밀 값 관리, rate limit, CORS)을 갖추고 싶다 | 기획 메모 | 2026-09-17 | promoted | → PRD-001, ADR-0004 |
| NB-014 | 직접 시나리오 테스트할 수 있는 가장 작은 단위로 구현하고 점진적으로 확장하고 싶다 | 기획 메모 | 2026-09-17 | promoted | → PRD 진행 원칙, CLAUDE.md |
| NB-015 | 공용 데이터(공용 단어의 카테고리, 공용 혼동 관계)는 **admin만** 수정하고, 일반 유저는 자기 데이터만 바꾸게 하고 싶다 | 계획 검토 중 결정 | 2026-09-17 | promoted | → PRD-001, PRD-003 |
| NB-016 | 어떤 HSK 기준(HSK 2.0 1~3급 600단어 / HSK 3.0 1~3급 약 2,200단어)과 어떤 데이터 출처(라이선스)를 쓸지 정해야 한다. 한국어 발음·예문·혼동 관계는 공개 데이터에 거의 없어 직접 만들고 검토해야 한다 | 계획 검토 중 보류 | 2026-09-17 | hold | 단어 이슈(SRS-020) 착수 전 리포트로 결정 |
| NB-017 | 폰(Expo Go)에서 PC의 백엔드에 어떻게 접속할지(같은 Wi‑Fi LAN IP / 터널) 정해야 한다 | 계획 검토 | 2026-09-17 | promoted | 터널 2개(Expo `--tunnel` + cloudflared)로 확정 → [리포트](../reports/2026-09-20-phone-backend-access.md) |
| NB-018 | 나중에 refresh token rotation, 비밀번호 재설정, 2FA를 고려한다 | 기획 메모 | 2026-09-17 | hold | 1차 범위 밖 |
| NB-019 | 인증(회원가입·로그인) 작업을 **뒤로 미룬다**. 단어·퀴즈 기능을 먼저 만들어 보고, 인증은 직접 구현할지 외부 서비스(Clerk·Auth0·Supabase Auth 등)를 쓸지 그때 정한다 | 2026-09-24 사용자 결정 | 2026-09-24 | hold | 단어·퀴즈 1차 확인 후 재검토 |

## 부록: 기획 메모 원문 요약

### 유저 시나리오
| 시나리오 | 플로우 |
|---|---|
| 회원가입/로그인 | 이메일+비밀번호로 가입 → JWT 발급 → 이후 모든 요청에 토큰 첨부 |
| 단어 등록 | HSK 단어 일괄 등록, 필요시 커스텀 단어 추가 |
| 단어 메타데이터 | 단어에 카테고리 태그 부여, 예문·한국어 발음 표기 확인 |
| 단어 즐겨찾기 | 단어 목록/퀴즈 중 즐겨찾기 토글 → 즐겨찾기만 모아보기, 즐겨찾기 대상 퀴즈 |
| 일반 퀴즈 | 세션 시작 → mastery_score 낮은 단어 + 그 단어의 혼동 단어들을 조합해 문제 생성 → 답변 제출 → word_stats 갱신 → 다음 문제 |
| 수동 혼동 태깅 | 오답 시 "이 단어랑 헷갈렸어요" 선택 → confusion_links에 added_by=현재 유저로 생성 → 다음 문제부터 반영 |
| 오답노트/재도전 | 최근 세션들의 오답 문제만 모아 재도전 세션 시작(mode=review) |
| 타임어택 | mode=time_attack, 문제당 제한시간 내 응답 → response_time_ms 기록 → 정답률/평균 응답속도 집계 |
| 던전 모드 | mode=dungeon, 목숨/콤보/점수, 정해진 문제 수, 중간보스 문제 2개 |
| 학습 통계 | 유저별 word_stats 조회 → 취약 단어 목록, HSK 급수별 숙련도 |

모든 시나리오는 로그인한 유저의 `user_id` 컨텍스트 안에서만 동작하며, 다른 유저의 세션·통계는 조회할 수 없다.

### 원안 DB 스키마
| 테이블 | 주요 컬럼 | 비고 |
|---|---|---|
| USERS | user_id PK, email, password_hash, nickname, created_at | 인증 기준 |
| WORDS | word_id PK, owner_id FK(users, nullable), hanzi, pinyin, kr_pronunciation, meaning_kr, hsk_level, pos, example_sentence | owner_id=null이면 공용 마스터 |
| CATEGORIES | category_id PK, name | 공용 |
| WORD_CATEGORIES | word_id FK + category_id FK (복합 PK) | M:N 정션 |
| WORD_BOOKMARKS | user_id FK + word_id FK (복합 PK), created_at | 유저별 M:N 정션 |
| CONFUSION_LINKS | link_id PK, word_a_id FK, word_b_id FK, confusion_type, added_by FK(users, nullable) | words 자기참조 정션 |
| WORD_STATS | user_id FK + word_id FK (복합 PK), correct_count, wrong_count, mastery_score, last_reviewed_at | 유저별 분리의 핵심 |
| QUIZ_SESSIONS | session_id PK, user_id FK, mode, started_at, ended_at, lives_remaining, score, combo_streak | 유저 소유 |
| QUIZ_QUESTIONS | question_id PK, session_id FK, target_word_id FK, question_type, is_boss, is_correct, response_time_ms | 세션을 통해 유저에 귀속 |
| QUESTION_CHOICES | choice_id PK, question_id FK, word_id FK, is_answer | 문제-보기 M:N 정션 |

보강안은 [arc42 5절 ERD](../architecture/arc42.md#5-빌딩-블록)에 반영했다.

### 원안 API
| 엔드포인트 | 설명 | 우선순위 |
|---|---|---|
| POST /auth/register, /auth/login, /auth/refresh | 인증 | 1차 |
| GET /words?hsk_level=&category=&bookmarked= | 단어 목록 | 1차 |
| POST /words | 커스텀 단어 추가 | 1차 |
| POST /words/{id}/categories | 카테고리 태그 | 1차 |
| PUT/DELETE /words/{id}/bookmark | 즐겨찾기 토글 | 1차 |
| POST /quiz/sessions | 세션 시작 | 1차(normal만) |
| GET /quiz/sessions/{id}/next-question | 다음 문제 | 1차 |
| POST /quiz/sessions/{id}/answer | 답변 제출 | 1차 |
| POST /quiz/sessions/{id}/complete | 세션 종료 | 1차 |
| POST /confusion-links | 수동 혼동 태깅 | 2차 |
| GET /users/me/stats | 내 학습 통계 | 2차 |

### 던전 모드 텍스트 피드백 예시
- 상단 상태: `♥♥♡ · 콤보 x4 · 1250점`
- 오답: `-1 목숨! 헷갈렸던 단어: 买 vs 卖`
- 중간보스: `중간보스! 3개 중 정답을 고르세요`
