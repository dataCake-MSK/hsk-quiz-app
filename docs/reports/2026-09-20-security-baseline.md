# 리포트: 보안 점검과 향후 작업에 적용할 기준

- 작성: 2026-09-20
- 상태: 확정(일부 결정 필요)
- 관련: NB-013, ADR-0004, SRS-003, SRS-014(이슈 #9)
- 범위: ① 공개(Public) 저장소를 쓰기 때문에 생기는 것 ② 이 프로젝트 전반(앱·API·개발 환경)

## 1. 요약
- 지금까지 조치: secret scanning·push protection, `.env` 커밋 금지, ORM 사용, 남의 리소스 404, rate limit·CORS(이슈 #9), 커밋 전 비밀 값 패턴 점검.
- 이번에 추가: **Dependabot 알림·보안 업데이트 활성화**, **Stop 훅의 비밀 값 스캔**, **CLAUDE.md 보안 점검 항목**(모든 이슈에 적용), PR 템플릿 보안 체크.
- 사용자가 결정할 것: ① 커밋 이메일을 GitHub noreply로 바꿀지 ② main 브랜치 보호 규칙을 켤지 ③ CI에 gitleaks·CodeQL을 넣을지.

## 2. 공개 저장소이기 때문에 생기는 것

| # | 위험 | 현재 | 조치 |
|---|---|---|---|
| P1 | 커밋된 비밀 값은 **되돌려도 기록에 남는다**(GitHub는 push 전 차단만 해줌) | push protection 켬 | 커밋 전 패턴 점검 + Stop 훅 스캔 추가. 유출되면 **키를 먼저 폐기**하고 기록 정리 |
| P2 | 코드·문서·이슈·PR·일지가 **전부 공개**된다 | 규칙 있음 | 개인 정보(집 네트워크 IP, 터널 주소, 실제 이메일, 스크린샷)를 문서에 쓰지 않는다 |
| P3 | **커밋 작성자 이메일이 공개**된다. 지금 로컬 커밋에 개인 Gmail 주소가 들어가 있다 | 노출 중 | 아래 3절 결정 필요 ① |
| P4 | 누구나 fork·PR을 열 수 있다. 악의적 PR이 CI에서 코드를 실행할 수 있음 | CI 없음(이슈 #3) | CI는 `pull_request`만 쓰고 `pull_request_target` 금지, `permissions: read-all` 기본(현재 기본값 read 확인됨), 포크 PR에는 시크릿을 주지 않음 |
| P5 | 의존성 취약점이 공개적으로 노출됨 | **Dependabot 알림·보안 업데이트 켬** | 알림이 오면 이슈로 만들어 처리 |
| P6 | 제네릭 비밀 값 패턴 검사(non-provider patterns)는 이 플랜에서 켜지지 않음 | disabled | CI에 gitleaks 추가로 보완(결정 ③) |

## 3. 결정 필요

**① 커밋 이메일** — 지금 로컬 커밋 작성자는 개인 Gmail이고, 머지 커밋은 GitHub noreply다. 앞으로를 noreply로 바꾸려면:
```bash
git config --global user.email "59680837+dataCake-MSK@users.noreply.github.com"
```
GitHub → Settings → Emails에서 "Keep my email addresses private"와 "Block command line pushes that expose my email"도 함께 켜는 것을 권한다. **과거 커밋까지 바꾸려면 기록 재작성이 필요**하므로 따로 결정한다.

**② main 브랜치 보호** — 공개 저장소는 무료로 ruleset을 쓸 수 있다. "PR 없이는 main에 push 금지"만 켜면 지금 작업 방식과 충돌하지 않는다. 리뷰 승인 필수까지 켜면 1인 개발에서는 🟢 자체 머지가 막힌다.

**③ CI 보안 단계(이슈 #3에 포함)** — gitleaks(비밀 값 스캔), `npm audit`·`uv pip audit`(의존성), CodeQL(공개 저장소 무료 정적 분석). 실행 시간이 늘어난다.

## 4. 프로젝트 전반 보안 기준 (모든 이슈에 적용)

| 영역 | 기준 | 확인 방법 |
|---|---|---|
| 인증 | 비밀번호 Argon2, JWT는 `JWT_SECRET`(없으면 시작 실패), access 15분·refresh 14일, 토큰 `type` 구분 | SRS-010~012 AC |
| 인가 | 유저 소유 리소스는 `user_id` 필터 필수, 남의 것은 404, 역할 부족은 403, 공용 데이터 변경은 admin만 | 이슈마다 "다른 유저 토큰 → 404" 테스트 |
| 입력 검증 | Pydantic 스키마로 타입·길이 제한, 정렬·필터 파라미터는 허용 목록 | 422 테스트 |
| 출력 | 오류 메시지에 내부 정보·존재 여부를 흘리지 않음(로그인 실패는 같은 문구) | SRS-011 AC |
| SQL | ORM만 사용, 문자열로 만든 raw SQL 금지 | 코드 리뷰 |
| 비밀 값 | `.env`에서만 읽기, `.env.example`엔 이름만, 로그·오류·일지에 출력 금지 | Stop 훅 스캔 + commit 스킬 |
| 의존성 | `uv.lock`·`package-lock.json` 커밋, Dependabot 알림 처리, 새 패키지는 PR에서 이유 설명 | 🟡 등급으로 사용자 확인 |
| 앱(Expo) | 토큰은 `expo-secure-store`, `EXPO_PUBLIC_*`에는 비밀 값 금지(번들에 그대로 들어감) | SRS-013 |
| 개발 서버·터널 | 터널이 켜진 동안 로컬 API가 인터넷에 공개됨 → 확인 끝나면 즉시 종료, 실데이터 없는 상태에서만 사용 | CLAUDE.md 서버 관리 규칙 |
| 요청 제한 | 공개 엔드포인트 `PUBLIC_RATE_LIMIT`, 인증 엔드포인트 `AUTH_RATE_LIMIT` | 이슈 #9 테스트 |
| CORS | 허용 출처는 환경 변수로 명시, 와일드카드 금지, 쿠키를 쓰지 않으므로 `allow_credentials=False` | 이슈 #9 테스트 |
| 배포(추후) | HTTPS 강제, `/docs` 공개 여부 재검토, 서버 로그에 토큰·비밀번호 남기지 않기 | 배포 이슈에서 |

## 5. 이번에 넣은 자동 조치
1. **Dependabot 알림 + 보안 업데이트**: 취약한 의존성이 생기면 GitHub가 알리고 PR을 만든다.
2. **Stop 훅 비밀 값 스캔**(`.claude/hooks/stop-vcs-check.js`): 턴을 끝내기 전에 작업 트리에서 키·토큰·DB 접속 문자열·개인 터널 주소 패턴을 찾으면 종료를 막고 알린다. 커밋 전에 걸러진다.
3. **CLAUDE.md 보안 점검 항목**: 이슈를 끝낼 때마다 위 4절 기준을 확인하도록 규칙에 명시.
4. **PR 템플릿**: 비밀 값·인가·의존성 체크 항목.

## 6. 유출이 의심될 때 (순서)
1. **키를 먼저 폐기·재발급**한다(기록 정리보다 우선).
2. 사용자에게 알리고, 어떤 값이 어디에 들어갔는지 정리한다.
3. 필요하면 기록 재작성(`git filter-repo`)과 강제 push를 사용자 승인 후 진행한다.
4. 재발 방지 조치를 이 리포트에 `## 갱신`으로 추가한다.

## 참고
- GitHub secret scanning: https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning
- Dependabot 알림: https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts
- GitHub Actions 보안 강화: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors/
- Expo 환경 변수: https://docs.expo.dev/guides/environment-variables/
- OWASP API Security Top 10: https://api-security.owasp.org/editions/2023/en/0x11-t10/
