---
name: commit
description: 변경 사항을 목적별 Conventional Commit으로 나누고 브랜치 push → PR → 머지 등급 판단 → 머지·브랜치 삭제 → 요약 보고까지 형상관리 전체를 처리한다. "커밋해줘", "PR 올려줘", "머지해줘", 작업 단위 완료 후, 또는 Stop 훅이 형상관리 누락을 알렸을 때 사용.
---

# commit — 자동 형상관리

## 원칙
- main에 직접 커밋·push 하지 않는다.
- 머지 여부는 `CLAUDE.md`의 **머지 등급**을 따른다.
- 비밀 값이 섞였으면 즉시 중단하고 사용자에게 알린다(Public 저장소).
- 사용자가 직접 작업 중인 것으로 보이는 무관한 변경은 커밋하지 않고 알린다.

## 절차
1. **상태 파악**: `git status`, `git diff`, `git diff --staged`, `git log --oneline -10`, 현재 브랜치, 열린 PR(`gh pr list --head <브랜치>`).
2. **비밀 값 점검**: 변경분(`git diff`, 새 파일)에서 아래를 찾는다. 테스트용 가짜 값이 명확하지 않으면 중단.
   - 패턴: `api[_-]?key`, `secret`, `token`, `password\s*=`, `Bearer `, `sk-`, `ghp_`, `gho_`, `github_pat_`, `JWT_SECRET\s*=\s*\S`, `postgres(ql)?(\+psycopg)?://[^/\s]*:[^@\s]*@`, 터널 URL(`trycloudflare.com`, `ngrok`), 개인 이메일, 긴 base64/hex 문자열
   - 파일: `.env`, `.env.*`(`.env.example` 제외), `*.pem`, `*.key`
3. **브랜치**: main이면 추적 ID·성격에 맞게 `feat|fix|docs|chore|refactor|test/SRS-xxx-짧은설명` 브랜치를 만든다. 추적 ID가 없으면 설명만.
4. **문서 동기화**(같은 PR에 포함)
   - 기능 변경 → `docs/requirements/SRS.md` AC 체크·상태, `traceability.md` 이슈·PR·상태
   - 오늘 커밋한 작업이 일지에 없으면 → `journal` 스킬
   - 사용자가 새로 알게 된 개념·시행착오 → `learn` 스킬
   - 계획·결정 상태가 바뀐 리포트 → `## 갱신 (YYYY-MM-DD)` 추가
   - 패턴·기술 결정을 새로 했으면 ADR이 있는지 확인
5. **목적별 분할 커밋**: 기능 / 테스트 / 리팩토링 / 문서 / 설정으로 나눈다. `git add <파일>`로 명시적 스테이징(`git add .` 금지).
6. **커밋 메시지**: `type(scope): 설명 (SRS-xxx)` — type은 feat, fix, docs, test, refactor, chore, ci. scope 예: auth, words, quiz, db, mobile, infra, requirements, architecture. 본문에 "왜"를 1~2줄. 시스템이 지정한 attribution 줄을 끝에 붙인다.
7. **push**: `git push -u origin <브랜치>`. push protection에 막히면 우회하지 말고 중단·보고.
8. **PR**: 열린 PR이 있으면 push로 끝. 없으면 `.github/pull_request_template.md` 형식으로 `gh pr create --body-file <임시파일>`(본문: `Closes #n`, 추적 ID, 수행한 테스트, **확인 방법**, 머지 등급과 이유).
   - PR 번호를 추적표에 적어야 하면 생성 후 번호를 확인해 추가 커밋·push.
9. **머지 등급 판단**(`CLAUDE.md` 표, 섞이면 높은 등급, 애매하면 한 단계 위)
   - 🟢 → CI가 있으면 `gh pr checks <n> --watch`로 통과 확인 → `gh pr merge <n> --merge --delete-branch` → `git switch main && git pull && git fetch --prune`
   - 🟡 / 🔴 → 머지하지 않고 사용자 확인 대기
10. **보고** (항상 **변경한 파일 표**부터: `파일 | 추가·수정·삭제 | 한 줄 설명`, 10개 초과면 묶어서 + 전체 개수)
    - 머지했으면: **변경** / **검증**(명령·결과) / **PR·이슈**(번호, 닫힌 이슈) / **브랜치 정리**(원격·로컬 삭제 여부)
    - 대기면: PR URL, 등급과 이유, 사용자가 확인할 점과 **확인 방법**(실행 명령, 눌러볼 화면, 확인할 응답)

## 인자
- `--no-pr`: push까지만
- `--local`: 커밋만(push·PR 없음)
- `--no-merge`: 🟢여도 머지하지 않음
