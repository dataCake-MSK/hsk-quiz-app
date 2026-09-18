---
name: issue
description: SRS·NB 문서 항목이나 대화 내용으로 GitHub 이슈를 만들고 라벨·마일스톤을 붙인 뒤 SRS·추적표에 이슈 번호를 기록한다. "이슈 만들어줘", "SRS 이슈로 등록", "니즈 적어둬", "NB로 적어줘" 요청 시 사용. 리포트 작성은 report 스킬.
---

# issue — 이슈 생성과 추적성 관리

> "이슈"는 GitHub 이슈만 가리킨다.

## 모드
- `srs <ID...|m0|m1|all>`: SRS 항목을 이슈로 등록(`planned` 상태는 사용자가 명시할 때만)
- `nb "<내용>"`: 니즈를 `docs/requirements/NB.md`에 새 NB 항목으로 추가하고 `type:needs` 이슈 생성

## srs 절차
1. `docs/requirements/SRS.md`에서 대상 항목(작업·AC·추적·선행)을 읽는다.
2. **중복 확인**: `gh issue list --state all --search "SRS-xxx in:title" --json number,title`. 있으면 새로 만들지 않고 번호만 기록.
3. [SRS-to-issue.md](SRS-to-issue.md) 형식으로 본문을 임시 파일(스크래치패드)에 쓰고, 제목은 `[SRS-xxx] 제목`.
4. 라벨·마일스톤은 `SRS-to-issue.md`의 매핑을 따른다. 라벨·마일스톤이 없으면 먼저 만든다.
5. `gh issue create --title ... --body-file <임시파일> --label ... --milestone ...`
6. AC가 자동으로 확인 가능하면(API·테스트만으로 확인, 실기기·사용자 작업 불필요, 🔴 아님) 사용자에게 `loop-ready` 라벨을 **제안만** 한다. 사용자가 요청하면 붙인다.
7. `SRS.md` 항목의 `이슈: -`와 목록 표의 이슈 칸, `traceability.md`의 이슈 칸을 `#n`으로 갱신.
8. 문서 변경은 `commit` 스킬로 커밋(번호 반영만이면 🟢).
9. 보고: 만든 이슈 번호·제목 표, 건너뛴 중복, loop-ready 제안.

## nb 절차
1. `NB.md` 표의 마지막 번호 + 1로 항목 추가(출처, 등록일 오늘, 상태 `new`).
2. `gh issue create --title "[NB-xxx] 요약" --label type:needs`로 이슈 생성, 본문에 NB ID와 원문.
3. PRD 승격이 필요해 보이면 제안만 한다(PRD는 사용자가 결정).
4. `commit` 스킬로 커밋.
