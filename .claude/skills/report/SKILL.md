---
name: report
description: 개발 진행 계획, 진행 현황, 기술·체계 검토 결과를 docs/reports/ 리포트로 작성·갱신한다. "리포트", "리포트로 남겨줘", "검토해서 정리", "진행 계획 정리", "현황 정리" 요청 시 사용. GitHub 이슈 생성은 issue 스킬.
---

# report — 리포트 작성

> "이슈"는 GitHub 이슈만 가리킨다. 이 스킬의 결과물은 "리포트"다.

## 인자
- 주제(예: `HSK 데이터 출처 검토`, `폰 접속 방식`, `M1 현황`)

## 절차
1. **사실 수집 — 추측하지 않는다.**
   - 현황: `gh issue list --state all --json number,title,state,labels,milestone,updatedAt --limit 200`, `gh pr list --state all --limit 50 --json number,title,state,mergedAt`, `gh api repos/{owner}/{repo}/milestones`
   - 요구사항: `docs/requirements/SRS.md`, `traceability.md`, 관련 ADR
   - 외부 기술 검토: 공식 문서를 WebFetch/WebSearch로 확인하고 링크를 남긴다. 확인하지 못한 내용은 "확인 필요"로 표시.
2. 같은 주제의 리포트가 이미 있으면 새 파일 대신 그 파일에 `## 갱신 (YYYY-MM-DD)` 섹션을 추가한다.
3. 새 리포트는 `docs/reports/YYYY-MM-DD-<주제-kebab-case>.md`.
   - 첫 줄 `# 리포트: <제목>`, 다음에 작성일·상태(제안/확정/완료)·관련 이슈/SRS
   - 구성: **요약 → 현황 → 분석/계획 → 결정 필요 → 참고**
   - 사용자가 폰(GitHub 모바일)으로 읽으므로 표·짧은 문장 위주, 도식은 Mermaid 우선(필요 시 PlantUML 병기)
   - Public 저장소: 비밀 값·개인 URL·로컬 접속 정보 금지
4. `docs/reports/README.md` 목록(날짜·링크·상태)을 갱신한다.
5. 결정 필요 사항이 있으면 응답에서 사용자에게 짧게 묻는다.
6. 형상관리는 `commit` 스킬(리포트만 바뀌었으면 🟢).
