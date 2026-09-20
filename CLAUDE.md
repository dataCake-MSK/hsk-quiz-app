# CLAUDE.md

HSK 1~3급 혼동 단어 기반 개인용 중국어 퀴즈 앱. FastAPI(`backend/`) + Expo/React Native(`mobile/`) + PostgreSQL. 1인 개발, **Public 저장소**.

학습 목표: ① DB 설계 ② 클린 아키텍처·디자인 패턴 ③ 배포 대비 최소 보안. 구현할 때 이 목표를 설명할 기회로 삼는다(왜 이 제약·계층·검사가 필요한지 짧게).

## 작업 방식
- 사용자는 주로 폰(Claude 앱 Remote Control, GitHub 모바일)에서 지시·확인한다. 폰에서 보낸 `!` 명령은 실행되지 않으므로, 대화형 로그인·설치는 **PC 별도 터미널에서 실행할 정확한 명령**이나 기기 코드 방식으로 안내한다.
- 기본: 이슈 단위 대화형 진행 → 결과 보고 → 다음 지시. 지시 범위를 넘는 작업은 하지 않는다.
- `/loop`: `loop-ready` 라벨이 붙은 이슈만, 번호 오름차순으로 1개씩. 이슈당 브랜치 1개·PR 1개. 테스트·CI가 2번 실패하거나 AC가 모호하면 이슈에 코멘트를 남기고 중단.
- 사실은 추측하지 않고 확인한다(공식 문서, `gh` 조회, 실제 실행). 확인하지 못한 것은 "확인 필요"로 표시.

## 구현 단위와 패턴
- **구현 단위는 사용자가 직접 시나리오 테스트할 수 있는 최소 크기로 자른다.** 여러 기능을 한 PR에 묶지 않는다.
- 이슈가 끝나면 **확인 방법**(실행 명령, 눌러볼 화면, 확인할 응답)을 함께 보고한다.
- **디자인 패턴은 필요해진 시점에 리팩토링으로 도입하고, 도입 이유를 ADR로 남긴다.** 아직 불필요한 패턴은 불필요하다고 말한다. 도입 시점 기준은 [ADR-0003](docs/architecture/adr/0003-clean-architecture-layers.md).
- 계층: `domain` ← `application`(유스케이스, `ports/`) ← `interface`(라우터, DTO) ← `infrastructure`(SQLAlchemy, JWT, 설정). 안쪽 계층은 바깥 계층을 import하지 않는다.

## 용어
- **이슈** = GitHub 이슈만 가리킨다. 저장소에 `issue` 폴더를 만들지 않는다.
- **리포트** = `docs/reports/`의 계획·현황·검토 문서. "정리해줘", "검토해서 남겨줘", "진행 계획", "현황"은 리포트 요청으로 본다(`report` 스킬).
- **일지** = `docs/journal/YYYY-MM-DD.md`, **학습 노트** = `docs/learning/`.

## 자동 형상관리 (요청이 없어도 Claude가 끝까지 처리)
Stop 훅(`.claude/hooks/stop-vcs-check.js`)이 턴 종료 시 커밋 안 된 변경, push 안 된 커밋, 오늘 일지 누락을 점검해 남아 있으면 종료를 막는다.

1. 파일을 바꾸는 작업은 브랜치에서 한다. **main 직접 커밋·push 금지.**
2. 작업 단위가 끝나면 `commit` 스킬로 목적별 Conventional Commit → push → PR.
3. 같은 PR에 문서 동기화를 포함한다.
   - 추적: SRS AC 체크, `traceability.md` 이슈·PR·상태
   - 일지: `journal` 스킬로 오늘 일지 갱신(하단 "개발자 퀵 가이드": 시행착오 제외, 실제로 효과 있었던 진행사항·명령·코드만)
   - 학습: 사용자가 새로 알게 된 개념·시행착오가 있으면 `learn` 스킬
   - 리포트: 계획·결정 상태가 바뀌었으면 `## 갱신 (날짜)` 추가
4. 아래 머지 등급에 따라 머지하거나 사용자 머지를 기다린다.
5. 머지하면 `gh pr merge <n> --merge --delete-branch` 후 **변경 / 검증 / PR·이슈 / 브랜치 정리** 순서로 요약 보고.

### 보고 형식 (모든 작업 후, 요청이 없어도)
- **변경한 파일 요약**을 항상 표로 보여준다: `파일 경로 | 추가·수정·삭제 | 한 줄 설명`. 파일이 10개를 넘으면 폴더·목적 단위로 묶고 전체 개수를 함께 적는다(`git status --short`, `git diff --stat` 기준).
- 이어서 **확인 방법**(실행 명령, 눌러볼 화면, 확인할 응답)과 **사용자가 결정할 것**을 적는다.
- 문서 동기화(추적표·일지·학습 노트·리포트)에서 무엇을 갱신했는지 한 줄로 밝힌다.
- **PR을 보여줄 때는 GitHub 링크 바로 아래에 PR 요약을 붙인다.** 사용자가 링크를 열지 않고 이 요약만 보고 머지를 요청할 수 있어야 한다.
  ```
  PR #n: <링크>
  - 무엇을·왜: 1~2줄
  - 주요 변경: 3~5줄
  - 검증: 실행한 명령과 결과
  - 확인할 점: 사용자가 판단할 것 (없으면 "없음")
  - 머지 등급: 🟢/🟡/🔴 + 이유
  ```

### 머지 등급
| 등급 | 대상 | 처리 |
|---|---|---|
| 🟢 AI 자체 머지 | 문서만 변경(일지·학습 노트·리포트·README, 추적 문서의 번호·체크 반영) / 사용자가 확인하고 머지를 요청한 PR / (CI 도입 후) 테스트만 추가, 동작 무변경 lint·포맷 | CI가 있으면 통과 확인 후 머지 + 요약 보고 |
| 🟡 사용자 머지 | 앱 동작·화면 변경, 의존성 추가·변경, PRD·SRS 내용(범위·AC) 변경, ADR 신규·변경 | PR까지 만들고 확인할 점(확인 방법 포함) 보고 |
| 🔴 사전 확인 | 작업 규칙·자동화(`CLAUDE.md`, `.claude/`, `.github/workflows`), 보안·인증·인가, 대량 삭제, 저장소 설정, 배포, 유료·외부 서비스 | **착수 전에 질문**, PR은 사용자 머지 |

- 한 PR에 등급이 섞이면 가장 높은 등급을 따른다.
- 애매하면 한 단계 높은 등급으로 처리한다.
- 인증·인가 기능 이슈(SRS-010~014 등)는 🔴이지만, 사용자가 이슈 진행을 지시한 것을 착수 확인으로 본다.

## 요구사항·추적성
- 문서: `docs/requirements/` NB(니즈 덤프) → PRD(무엇을, 사람 중심) → SRS(어떻게, AI 중심, AC) → `traceability.md`
- ID: `NB-001`, `PRD-001`, `SRS-001`, `ADR-0001`. **SRS 1개 = 이슈 1개 = PR 1개.** 이슈 제목 `[SRS-xxx] ...`, PR 본문에 `Closes #n`과 추적 ID.
- 구현 중 요구사항이 바뀌면 SRS를 먼저 고치고, 제품 범위가 바뀌면 PRD 변경을 제안한다(PRD는 사용자가 결정).
- 되돌리기 어려운 기술 선택은 `docs/architecture/adr/`에 ADR 작성(템플릿 `0000-template.md`).

## Git 규칙
- 브랜치: `feat/SRS-010-register-api`, `fix/…`, `docs/…`, `chore/…`, `refactor/SRS-025-repository`
- 커밋: Conventional Commits(`feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`), 한국어 설명. 예: `feat(auth): 회원가입 API 추가 (SRS-010)`
- `git add <파일>`로 명시적 스테이징(`git add .` 금지). 머지 방식은 merge commit(`--merge`).
- 스킬: 커밋·PR·머지 `commit`, 이슈·NB `issue`, 리포트 `report`, 일지 `journal`, 학습 노트 `learn`.

## 보안 (Public 저장소)
> 기준과 배경은 [보안 리포트](docs/reports/2026-09-20-security-baseline.md). **모든 이슈에서 아래 점검을 거친다.**

### 이슈를 끝낼 때 보안 점검 (해당하는 항목만, PR 본문에 결과 기재)
1. 비밀 값이 코드·문서·로그·테스트에 들어가지 않았는가 (Stop 훅이 작업 트리를 자동 스캔한다)
2. 유저 소유 리소스에 `user_id` 필터가 걸렸는가, 남의 것은 404인가 — 해당 테스트를 추가했는가
3. 입력을 Pydantic으로 검증했는가, 오류 메시지가 내부 정보·존재 여부를 흘리지 않는가
4. 새 의존성을 추가했다면 이유가 PR에 있는가 (🟡 이상)
5. 새 엔드포인트라면 인증 필요 여부와 rate limit 대상인지 판단했는가
6. 앱이면 토큰을 `expo-secure-store`에 넣었는가, `EXPO_PUBLIC_*`에 비밀 값이 없는가

### 항상
- 비밀 값(키·토큰·비밀번호·DB 접속 문자열·터널 URL·개인 이메일)은 코드·문서·일지·커밋 메시지에 넣지 않는다. 커밋 전 패턴 점검(`commit` 스킬). 의심되면 중단하고 알린다.
- 유출이 의심되면 **키 폐기·재발급이 먼저**, 그다음 기록 정리(사용자 승인 후).
- CI는 `pull_request` 트리거만 쓰고 `pull_request_target`·포크 PR에 시크릿 노출을 만들지 않는다.
- Dependabot 알림이 오면 이슈로 만들어 처리한다.
- `.env*`는 커밋 금지, `.env.example`에는 변수 이름만.
- GitHub secret scanning·push protection 사용. push가 차단되면 우회하지 말고 사용자에게 알린다.
- 인가 규칙([ADR-0004](docs/architecture/adr/0004-auth-and-identifiers.md))
  - 유저 소유 리소스(word_stats, word_bookmarks, quiz_sessions, 커스텀 단어 등)는 항상 `user_id = :current_user` 조건을 거친다. Repository 도입(SRS-025) 후에는 Repository 메서드의 필수 인자로 강제하고 우회 경로를 만들지 않는다.
  - 남의 리소스 접근은 404, 역할 부족은 403. 유저 소유 API마다 "다른 유저 토큰 → 404" 테스트를 둔다.
  - 공용 데이터(공용 단어 카테고리, 공용 혼동 관계) 변경은 `role = admin`만.
- ORM(SQLAlchemy) 사용, raw SQL 문자열 조합 금지.

## 도식
- 기본은 Mermaid(GitHub 모바일에서 렌더링). 표현력이 더 필요하면 PlantUML(```plantuml 블록)을 병기하되 핵심 그림은 Mermaid로도 제공.

## 개발 명령
> 스캐폴딩(SRS-001·002) 전이라 아직 없는 명령이 있다. 해당 이슈에서 실제 명령으로 갱신한다.

| 대상 | 명령 |
|---|---|
| 백엔드 실행 | `cd backend && uv run fastapi dev app/main.py` |
| 백엔드 테스트 | `cd backend && uv run pytest` |
| 백엔드 lint | `cd backend && uv run ruff check .` |
| 마이그레이션 | `cd backend && uv run alembic upgrade head` (SRS-004 이후) |
| 앱 실행(폰 확인) | `cd mobile && npx expo start --tunnel --go` (8081이 사용 중이면 `--port 8082`) |
| 앱 타입 검사 | `cd mobile && npx tsc --noEmit` |
| 백엔드 터널 | `cloudflared tunnel --url http://localhost:8000 --no-autoupdate` |

- Expo는 SDK마다 API가 바뀌므로 코드 작성 전 해당 버전 문서를 확인한다. 현재 SDK 57.
- **폰 확인은 터널 2개**(Expo Metro + 백엔드 API)가 필요하다. 절차와 주의점은 [리포트](docs/reports/2026-09-20-phone-backend-access.md).
  - 백엔드 터널 주소는 실행할 때마다 바뀌므로 `mobile/.env`의 `EXPO_PUBLIC_API_URL`을 갱신하고 Expo를 다시 시작한다.
  - 백그라운드로 띄우면 주소가 로그에 안 나온다. Expo 주소는 `curl -s http://127.0.0.1:4040/api/tunnels`의 `public_url`(다른 Expo가 떠 있으면 4041…)을 `exp://`로 바꿔 전달한다.
  - 터널 주소·Expo 주소는 개인 URL로 취급해 문서·커밋·일지에 쓰지 않는다(채팅으로만 전달).
- **오래 켜둔 서버는 계속 켤지 묻는다.** 대상: Expo 개발 서버(Metro, Expo Go 미리보기), FastAPI 개발 서버, 터널.
  - 켤 때 시작 시각을 적어두고, **확인이 끝났을 때** 또는 **약 30분이 지났을 때** "계속 켜둘까요, 끌까요?"라고 묻는다. 계속 켜기로 하면 그 뒤로도 약 30분마다 다시 묻는다.
  - 사용자가 답하기 전에 **자동으로 끄지 않는다.**
  - 끌 때는 백그라운드 작업을 중지하고 포트(8000, 8081)·프로세스가 남지 않았는지 확인해 보고한다.
  - 세션이 길어지면 `/loop 30m 켜둔 개발 서버 계속 켤지 확인` 같은 방법으로 확인 시점을 놓치지 않는다.

## 환경 메모
- Windows 11. 셸은 PowerShell과 Git Bash.
- 도구: gh(로그인됨, `repo`·`workflow` scope), Node 22, Python 3.12, uv.
- PostgreSQL은 사용자 PC에 직접 설치(SRS-004 전). Docker 없음.
