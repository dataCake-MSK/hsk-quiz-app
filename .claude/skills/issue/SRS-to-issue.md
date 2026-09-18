# SRS 항목 → 이슈 본문 형식

```markdown
### 추적 ID
NB-xxx → PRD-xxx → SRS-xxx

### 작업 내용
(SRS 항목의 작업 목록)

### 수용 기준 (AC)
- [ ] ...

### 확인 방법
(사용자가 직접 확인할 명령·화면·응답. AC에 이미 있으면 "AC 참고")

### 메모 / 제약
- 문서: docs/requirements/SRS.md 의 SRS-xxx
- 선행: (있으면)
- 머지 등급 예상: 🟢/🟡/🔴 와 이유
- 패턴: (도입하는 패턴이 있으면 ADR 번호, 없으면 "도입 없음")
```

## 라벨 매핑
| 조건 | 라벨 |
|---|---|
| 기능 | `type:feature` |
| 리팩토링·설정·CI·스캐폴딩 | `type:chore` |
| 문서 | `type:docs` |
| 버그 | `type:bug` |
| SRS 목록의 area 칸 | `area:auth`, `area:words`, `area:quiz`, `area:db`, `area:mobile`, `area:infra` |
| M0 전체, MVP 핵심 흐름(인증·단어 목록·퀴즈 SRS-030~033) | `priority:high` |
| 그 밖의 M1 | `priority:low` |

## 마일스톤 매핑
| SRS 목록의 M 칸 | 마일스톤 |
|---|---|
| M0 | `M0 기반` |
| M1 | `M1 MVP` |
| 2차·3차 | 마일스톤 없음(이슈 등록 시 사용자와 결정) |
