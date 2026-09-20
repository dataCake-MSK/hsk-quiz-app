# SRS — HSK Quiz App

- 버전: v0 (2026-09-17)
- 소유: AI 중심 (PRD 범위 안에서 작성, 범위를 바꾸려면 PRD를 먼저 고침)
- 규칙: **SRS 1개 = 이슈 1개 = PR 1개**. 각 항목은 사용자가 직접 눌러보거나 호출해서 확인할 수 있는 크기다.
- AC는 확인 가능한 문장으로 쓴다. PR이 머지되면 AC를 체크하고 [추적표](traceability.md)를 갱신한다.
- 공통 AC(모든 기능 항목에 적용, 항목마다 반복하지 않음)
  - CI가 도입된 뒤(SRS-003)에는 CI 통과
  - 유저 소유 리소스는 다른 유저 토큰으로 접근하면 404
  - 비밀 값은 `.env`에서만 읽고, `.env.example`에는 이름만 남김

## 목록
| ID | M | 제목 | PRD | area | 상태 | 이슈 |
|---|---|---|---|---|---|---|
| SRS-001 | M0 | 백엔드 스캐폴딩과 health API | 기반 | infra | done | #1 |
| SRS-002 | M0 | Expo 앱 스캐폴딩과 백엔드 연결 확인 | 기반 | mobile | todo | #2 |
| SRS-003 | M0 | CI (backend lint·test, mobile typecheck·lint) | 기반 | infra | todo | #3 |
| SRS-004 | M0 | PostgreSQL 연결, 마이그레이션 도구, users 테이블 | 기반 | db | todo | #4 |
| SRS-010 | M1 | 회원가입 API | PRD-001 | auth | todo | #5 |
| SRS-011 | M1 | 로그인 API와 내 정보 조회 | PRD-001 | auth | todo | #6 |
| SRS-012 | M1 | 토큰 갱신 API | PRD-001 | auth | todo | #7 |
| SRS-013 | M1 | 앱 가입·로그인 화면과 토큰 보관 | PRD-001 | mobile | todo | #8 |
| SRS-014 | M1 | 인증 엔드포인트 rate limit과 CORS | PRD-001 | auth | in-progress | #9 |
| SRS-020 | M1 | 단어 테이블, 샘플 시드, 단어 목록 API | PRD-002 | words | todo | #10 |
| SRS-021 | M1 | 앱 단어 목록·상세 화면 | PRD-002, PRD-003 | mobile | todo | #11 |
| SRS-022 | M1 | 커스텀 단어 추가 | PRD-002 | words | todo | #12 |
| SRS-023 | M1 | 카테고리 태그와 필터 | PRD-003 | words | todo | #13 |
| SRS-024 | M1 | 단어 즐겨찾기 | PRD-004 | words | todo | #14 |
| SRS-025 | M1 | 리팩토링: Repository 패턴 도입 | PRD-004 | db | todo | #15 |
| SRS-030 | M1 | 혼동 관계 시드와 퀴즈 세션 시작 | PRD-005 | quiz | todo | #16 |
| SRS-031 | M1 | 다음 문제 생성 (혼동 단어 보기) | PRD-005 | quiz | todo | #17 |
| SRS-032 | M1 | 답변 제출과 숙련도 갱신 | PRD-005 | quiz | todo | #18 |
| SRS-033 | M1 | 세션 종료와 결과 화면 | PRD-005 | quiz | todo | #19 |
| SRS-034 | M1 | 즐겨찾기 퀴즈 + Strategy 패턴 도입 | PRD-004, PRD-005 | quiz | todo | #20 |
| SRS-035 | M1 | 뜻→단어 문제 유형 + Factory 패턴 도입 | PRD-005 | quiz | todo | #21 |
| SRS-040 | 2차 | 수동 혼동 태깅 | PRD-006 | quiz | planned | - |
| SRS-041 | 2차 | 오답노트/재도전 세션 | PRD-007 | quiz | planned | - |
| SRS-042 | 2차 | 내 학습 통계 | PRD-008 | quiz | planned | - |
| SRS-050 | 3차 | 타임어택 모드 | PRD-009 | quiz | planned | - |
| SRS-051 | 3차 | 던전 모드 | PRD-010 | quiz | planned | - |

---

## M0 기반

### SRS-001 백엔드 스캐폴딩과 health API
- 추적: 기반 · 이슈: #1
- 작업
  - `backend/`에 uv 프로젝트 생성, FastAPI 설치
  - 4계층 폴더: `app/domain`, `app/application`, `app/interface`, `app/infrastructure` (빈 패키지 + 각 `__init__.py` docstring으로 책임 설명) — [ADR-0003](../architecture/adr/0003-clean-architecture-layers.md)
  - `GET /health` → `{"status": "ok"}`
  - pytest, ruff 설정
- AC
  - [x] `cd backend && uv run fastapi dev app/main.py` 실행 후 `curl http://127.0.0.1:8000/health`가 `{"status":"ok"}`
  - [x] `uv run pytest`에서 health 테스트 1개 통과
  - [x] `uv run ruff check .` 오류 0
  - [x] `http://127.0.0.1:8000/docs`에 `/health`가 보임

### SRS-002 Expo 앱 스캐폴딩과 백엔드 연결 확인
- 추적: 기반, NB-017 · 이슈: #2
- 작업
  - `mobile/`에 Expo(TypeScript) 앱 생성(당시 최신 SDK, 버전 문서 확인)
  - 첫 화면에서 백엔드 `/health`를 호출해 결과 표시. API 주소는 `EXPO_PUBLIC_API_URL` 환경 변수
  - 폰에서 백엔드에 접속하는 방법(같은 Wi‑Fi LAN IP / 터널)을 실제로 확인하고 리포트에 기록
- AC
  - [ ] 폰 Expo Go에서 앱을 열면 화면에 `서버 상태: ok` 표시
  - [ ] 백엔드를 끄면 `서버에 연결할 수 없음` 표시
  - [ ] `npx tsc --noEmit` 오류 0
  - [ ] 접속 방식 결정이 `docs/reports/`에 기록됨

### SRS-003 CI
- 추적: 기반 · 이슈: #3
- 작업: `.github/workflows/ci.yml` — PR·main push 때 backend(`uv sync`, `ruff check`, `pytest`), mobile(`npm ci`, `tsc --noEmit`, `expo lint`) 실행. 바뀐 경로만 실행하도록 path 필터 사용
- AC
  - [ ] 이 PR에서 두 job이 모두 초록
  - [ ] 일부러 실패하는 테스트를 넣은 임시 커밋에서 CI가 빨강이 되는 것을 확인한 뒤 되돌림
  - [ ] `CLAUDE.md` 개발 명령에 CI와 같은 로컬 검증 명령 기재

### SRS-004 PostgreSQL 연결, 마이그레이션 도구, users 테이블
- 추적: 기반, PRD-001 · 이슈: #4
- 선행: 사용자 PC에 PostgreSQL 설치 (안내는 이슈 착수 때 공식 문서 확인 후)
- 작업
  - SQLAlchemy 2 + psycopg, Alembic 설정. 접속 정보는 `DATABASE_URL` 환경 변수 — [ADR-0002](../architecture/adr/0002-postgresql-sqlalchemy-alembic.md)
  - `users`: `user_id BIGINT identity PK`, `email` (소문자 저장, UNIQUE), `password_hash`, `nickname`, `role` (`user`/`admin`, CHECK, 기본 `user`), `created_at timestamptz`
  - 테스트용 DB 분리(`TEST_DATABASE_URL`)
- AC
  - [ ] `uv run alembic upgrade head` 후 `psql`의 `\d users`에 위 컬럼·제약이 보임
  - [ ] `uv run alembic downgrade base`가 오류 없이 되돌림
  - [ ] `GET /health`가 DB 연결 상태를 `{"status":"ok","db":"ok"}`로 반환
  - [ ] `.env.example`에 변수 이름만 있음

## M1 MVP — 인증 (PRD-001)

### SRS-010 회원가입 API
- 추적: NB-002 → PRD-001 · 이슈: #5
- 작업: `POST /auth/register` {email, password, nickname}. 비밀번호는 argon2 해싱 — [ADR-0004](../architecture/adr/0004-auth-and-identifiers.md). **SRS-014에서 준비한 `AUTH_RATE_LIMIT`을 이 라우터에 적용**하고 6번째 요청 → 429 테스트 추가
- AC
  - [ ] 정상 요청 → 201, 응답에 `user_id`, `email`, `nickname`만 있음(`password_hash` 없음)
  - [ ] 같은 이메일(대소문자만 다른 경우 포함) → 409
  - [ ] 비밀번호 8자 미만·이메일 형식 오류 → 422
  - [ ] DB의 `password_hash`가 `$argon2id$`로 시작
  - [ ] 위 경우를 pytest로 자동 검증

### SRS-011 로그인 API와 내 정보 조회
- 추적: NB-002 → PRD-001 · 이슈: #6
- 작업: `POST /auth/login` → `access_token`(15분), `refresh_token`(14일). `GET /users/me`. 공통 `get_current_user` 의존성. **`AUTH_RATE_LIMIT` 적용**(6번째 로그인 → 429 테스트)
- AC
  - [ ] 올바른 계정 → 200 + 두 토큰
  - [ ] 틀린 비밀번호와 없는 이메일이 **같은** 401 메시지
  - [ ] `GET /users/me`: 토큰 없음·만료·위조 → 401, 정상 → 내 정보(role 포함)
  - [ ] refresh 토큰으로 `/users/me` 호출 → 401 (토큰 `type` 구분)
  - [ ] JWT secret은 `JWT_SECRET` 환경 변수, 없으면 서버 시작 실패

### SRS-012 토큰 갱신 API
- 추적: PRD-001 · 이슈: #7
- 작업: `POST /auth/refresh` {refresh_token} → 새 access token
- AC
  - [ ] 유효한 refresh → 200 + 새 access
  - [ ] access 토큰을 넣음·만료·위조 → 401
  - [ ] 삭제된 유저의 refresh → 401

### SRS-013 앱 가입·로그인 화면과 토큰 보관
- 추적: PRD-001 · 이슈: #8
- 작업: 가입·로그인 화면, `expo-secure-store`에 토큰 저장, API 클라이언트가 access를 자동 첨부하고 401이면 refresh 한 번 시도, 로그아웃
- AC
  - [ ] 폰에서 가입 → 로그인 → 홈에 `안녕하세요, {닉네임}` 표시
  - [ ] 앱을 완전히 종료 후 다시 열어도 로그인 유지
  - [ ] 로그아웃 → 로그인 화면으로 이동, 토큰 삭제
  - [ ] 틀린 비밀번호 → 화면에 오류 문구

### SRS-014 인증 엔드포인트 rate limit과 CORS
- 추적: NB-013 → PRD-001 · 이슈: #9
- 작업
  - slowapi로 IP 기준 요청 제한. 설정값은 환경 변수 `PUBLIC_RATE_LIMIT`(기본 30/minute), `AUTH_RATE_LIMIT`(기본 5/minute)
  - CORS 허용 출처를 `CORS_ORIGINS` 환경 변수로(와일드카드 금지, `allow_credentials=False`)
  - **순서 변경**: 이 이슈를 인증(SRS-010·011)보다 먼저 진행했으므로, 지금은 공개 엔드포인트 `/health`에 `PUBLIC_RATE_LIMIT`을 적용해 동작을 확인한다. `AUTH_RATE_LIMIT`은 값만 준비해 두고 **SRS-010·011에서 `/auth/*`에 적용**한다(각 이슈의 작업 항목에 포함)
- AC
  - [x] 제한이 3/minute일 때 1분 안에 4번째 `/health` 요청 → 429, 본문은 `{"detail": ...}`
  - [x] 허용하지 않은 Origin의 preflight에 `Access-Control-Allow-Origin` 없음
  - [x] 허용한 Origin의 preflight에는 해당 헤더 있음
  - [x] `CORS_ORIGINS`가 비어 있으면 CORS 헤더를 붙이지 않음
  - [x] 위 경우를 pytest로 검증(`tests/test_rate_limit.py`, `tests/test_cors.py`)

## M1 MVP — 단어 (PRD-002, 003, 004)

### SRS-020 단어 테이블, 샘플 시드, 단어 목록 API
- 추적: NB-003 → PRD-002 · 이슈: #10
- 선행: NB-016(HSK 기준) 결정 전이면 **개발용 샘플 20단어**로 진행
- 작업
  - `words`: `word_id` PK, `owner_id` FK users NULL, `hanzi`, `pinyin`, `kr_pronunciation`, `meaning_kr`, `hsk_level` (CHECK 1~3), `pos`, `example_sentence`, `example_meaning_kr`
  - 시드 스크립트 `uv run python -m app.infrastructure.seed words` (여러 번 실행해도 중복 없음)
  - `GET /words?hsk_level=` (로그인 필요, `owner_id IS NULL OR owner_id = 나`)
- AC
  - [ ] 시드를 2번 실행해도 단어 수가 같음
  - [ ] `GET /words?hsk_level=1` → 1급 단어만
  - [ ] 토큰 없이 → 401
  - [ ] 응답 필드가 문서화된 스키마와 같음 (`/docs`)

### SRS-021 앱 단어 목록·상세 화면
- 추적: NB-003, NB-004 → PRD-002, PRD-003 · 이슈: #11
- AC
  - [ ] 목록 화면 상단의 1·2·3급 탭을 누르면 해당 급수 단어만 보임
  - [ ] 단어를 누르면 상세에 한자·병음·한국어 발음·뜻·예문·예문 뜻 표시
  - [ ] 로딩 중·빈 목록·오류 상태 문구가 각각 보임

### SRS-022 커스텀 단어 추가
- 추적: NB-003 → PRD-002 · 이슈: #12
- 작업: `POST /words` (owner_id = 나), 앱에 추가 화면
- AC
  - [ ] 추가한 단어가 내 목록에 보임
  - [ ] 다른 계정의 목록에는 안 보이고, 그 계정이 `GET /words/{id}` → 404
  - [ ] 필수 필드 누락 → 422, 화면에 오류 표시

### SRS-023 카테고리 태그와 필터
- 추적: NB-004, NB-015 → PRD-003 · 이슈: #13
- 작업
  - `categories`(공용, name UNIQUE), `word_categories`(word_id, category_id 복합 PK)
  - `POST /words/{id}/categories` — 공용 단어는 **admin만**, 커스텀 단어는 소유자만
  - `GET /words?category=`, 기본 카테고리 시드(운동/취미/여행 등), admin 계정 지정 스크립트
- AC
  - [ ] user가 공용 단어에 태그 → 403, 자기 커스텀 단어 → 200
  - [ ] admin이 공용 단어에 태그 → 200
  - [ ] 같은 태그를 두 번 달아도 중복 없음
  - [ ] 앱 목록에서 카테고리 필터가 동작

### SRS-024 단어 즐겨찾기
- 추적: NB-005 → PRD-004 · 이슈: #14
- 작업: `word_bookmarks`(user_id, word_id 복합 PK, created_at), `PUT/DELETE /words/{id}/bookmark`(멱등), `GET /words?bookmarked=true`, 목록·상세의 ☆/★ 토글, 즐겨찾기 탭
- AC
  - [ ] ☆를 누르면 ★로 바뀌고 앱을 다시 열어도 유지
  - [ ] PUT 두 번 → 둘 다 204, DELETE 두 번 → 둘 다 204
  - [ ] 즐겨찾기 탭에 내 즐겨찾기만 보임 (다른 계정 즐겨찾기 섞이지 않음)
  - [ ] 볼 수 없는 단어(남의 커스텀 단어) 즐겨찾기 → 404

### SRS-025 리팩토링: Repository 패턴 도입
- 추적: NB-012 → PRD-004 · 이슈: #15
- 도입 이유: 유저 소유 데이터(즐겨찾기)가 처음 생겨 **user_id 필터를 한 곳에서 강제**할 필요가 생기고, 유스케이스를 DB 없이 테스트하고 싶어짐
- 작업
  - `application/ports/`에 `WordRepository`, `BookmarkRepository` (Protocol), `infrastructure/repositories/`에 SQLAlchemy 구현
  - 유저 소유 조회 메서드는 `user_id`를 필수 키워드 인자로 받음
  - 라우터 → 유스케이스 → 포트 순서로 의존, `Depends()`로 구현 주입
  - ADR-0005 작성
- AC
  - [ ] 동작 변화 없음: 기존 API 테스트 전부 통과
  - [ ] 유스케이스 단위 테스트가 가짜(in-memory) 저장소로 DB 없이 통과
  - [ ] `app/application` 안에서 `sqlalchemy`·`fastapi` import 0건 (테스트로 검사)

## M1 MVP — 퀴즈 (PRD-005)

### SRS-030 혼동 관계 시드와 퀴즈 세션 시작
- 추적: NB-001 → PRD-005 · 이슈: #16
- 작업
  - `confusion_links`: `link_id` PK, `word_a_id`·`word_b_id` FK words, `confusion_type`(meaning/sound/shape), `added_by` FK users NULL, `CHECK (word_a_id < word_b_id)`, `UNIQUE NULLS NOT DISTINCT (word_a_id, word_b_id, added_by)` (공용 링크끼리도 중복 금지, PostgreSQL 15+)
  - `quiz_sessions`: `session_id` PK, `user_id` FK, `mode`(CHECK), `started_at`, `ended_at`, `lives_remaining`, `score`, `combo_streak`
  - 혼동 쌍 시드, `POST /quiz/sessions` {mode: normal}
- AC
  - [ ] 세션 생성 → 201 + `session_id`
  - [ ] `mode`가 normal이 아니면 422 (1차)
  - [ ] 같은 쌍을 순서만 바꿔 넣어도 1개로 저장
  - [ ] 앱 홈의 `퀴즈 시작` 버튼으로 세션이 생성됨

### SRS-031 다음 문제 생성 (혼동 단어 보기)
- 추적: NB-001 → PRD-005 · 이슈: #17
- 작업
  - `word_stats`(user_id, word_id 복합 PK, correct_count, wrong_count, mastery_score, last_reviewed_at), `quiz_questions`, `question_choices`
  - `GET /quiz/sessions/{id}/next-question`: 이 세션에서 아직 안 나온 단어 중 `mastery_score`가 가장 낮은 단어(기록 없으면 0)를 정답으로, 보기 4개 = 정답 + 그 단어의 혼동 단어(공용 + 내가 추가한 것) 최대 3개 + 부족하면 같은 급수 무작위. 보기 순서는 섞음
  - 문제 유형은 **단어→뜻 1개만** (Factory 불필요)
- AC
  - [ ] 응답에 `question_id`, 한자·병음, 보기 4개(뜻)가 있고 **정답 여부는 없음**
  - [ ] 혼동 쌍이 있는 단어가 정답일 때 그 혼동 단어가 보기에 포함 (테스트)
  - [ ] 다른 유저의 세션 id → 404
  - [ ] 앱 퀴즈 화면에 문제와 보기 4개 표시

### SRS-032 답변 제출과 숙련도 갱신
- 추적: NB-001 → PRD-005 · 이슈: #18
- 작업
  - `POST /quiz/sessions/{id}/answer` {question_id, chosen_word_id, response_time_ms}
  - `quiz_questions`에 `chosen_word_id`, `is_correct`, `answered_at` 저장. 같은 문제를 다시 제출하면 409
  - 도메인 규칙 `domain/mastery.py`: 순수 함수로 새 mastery 계산(0~100)
- AC
  - [ ] 응답에 정답 여부와 정답 보기 id
  - [ ] 정답이면 `correct_count`+1·mastery 상승, 오답이면 `wrong_count`+1·mastery 하락
  - [ ] mastery 계산 함수 단위 테스트(경계값 0·100 포함)가 DB 없이 통과
  - [ ] 앱에서 보기를 누르면 정답/오답 표시 후 `다음 문제`로 진행

### SRS-033 세션 종료와 결과 화면
- 추적: PRD-005 · 이슈: #19
- 작업: `POST /quiz/sessions/{id}/complete` → `ended_at` 기록, 결과(문제 수·정답 수·정답률·틀린 단어 목록). 앱은 10문제 후 자동 종료
- AC
  - [ ] 10문제를 풀면 결과 화면에 `8/10 (80%)`와 틀린 단어 표시
  - [ ] 종료된 세션에 next-question·answer → 409
  - [ ] 두 번 complete → 같은 결과 반환(멱등)

### SRS-034 즐겨찾기 퀴즈 + Strategy 패턴 도입
- 추적: NB-005, NB-012 → PRD-004, PRD-005 · 이슈: #20
- 도입 이유: 출제 대상을 고르는 방식이 **2개**(혼동 기반 / 즐겨찾기)가 되어 분기 대신 교체 가능한 전략이 필요
- 작업: `QuestionSelectionStrategy` 포트 + `ConfusionBasedStrategy`, `BookmarkStrategy`. 세션에 `source`(all/bookmarked) 저장. ADR-0006
- AC
  - [ ] 즐겨찾기 탭의 `즐겨찾기로 퀴즈` → 정답 단어가 모두 즐겨찾기 단어
  - [ ] 즐겨찾기가 4개 미만이면 400과 안내 문구
  - [ ] 기존 퀴즈 테스트 전부 통과, 전략별 단위 테스트 추가

### SRS-035 뜻→단어 문제 유형 + Factory 패턴 도입
- 추적: NB-012 → PRD-005 · 이슈: #21
- 도입 이유: 문제 유형이 **2개**(단어→뜻 / 뜻→단어)가 되어 유형별 생성 로직을 분리할 필요
- 작업: `QuestionFactory`가 `question_type`에 따라 문제·보기 표시 방식 생성. 세션 안에서 유형을 섞음. ADR-0007
- AC
  - [ ] 한 세션에 두 유형이 모두 나옴 (테스트는 시드 고정)
  - [ ] 뜻→단어 문제는 뜻을 보여주고 보기로 한자+병음 표시
  - [ ] 기존 테스트 전부 통과

## 2차·3차 (planned, 이슈 미등록)
| ID | 요약 | 메모 |
|---|---|---|
| SRS-040 | `POST /confusion-links` — 오답 후 "이 단어랑 헷갈렸어요" → `added_by`=나로 저장, 본인 출제에만 반영 | admin이 만든 링크는 `added_by` NULL(공용) |
| SRS-041 | 최근 N개 세션의 오답으로 `mode=review` 세션 | Strategy 추가 |
| SRS-042 | `GET /users/me/stats` — 취약 단어, 급수별 평균 mastery | |
| SRS-050 | `mode=time_attack`, 문제당 제한시간, 평균 응답속도 집계 | |
| SRS-051 | `mode=dungeon`, 목숨·콤보·점수·중간보스 2개(보기 4개 이상, `is_boss`) | 텍스트 상태 표시줄 |
