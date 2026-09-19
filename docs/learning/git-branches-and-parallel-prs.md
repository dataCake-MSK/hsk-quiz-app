# Git 브랜치와 PR 여러 개 동시에 진행하기

## 핵심 개념
- **브랜치는 main의 특정 커밋에서 갈라져 나온 별도의 작업 줄기**다. 브랜치마다 커밋을 여러 개 쌓을 수 있고, PR은 "이 브랜치의 커밋들을 main에 합쳐 주세요"라는 요청이다.
- 브랜치 두 개가 **같은 파일의 같은 부분**을 서로 다르게 바꾸면 두 번째 머지에서 **충돌(conflict)**이 난다. 다른 파일을 바꾸거나, 같은 파일이라도 떨어진 부분을 바꾸면 Git이 자동으로 합친다.
- 충돌이 나도 PR 여러 개를 진행할 수 있다. 먼저 머지된 쪽은 그대로 들어가고, 나중 PR에서 충돌을 해결하는 커밋(main을 브랜치에 합치고 겹친 부분을 직접 고름)을 추가한 뒤 머지하면 된다. 충돌이 없으면 이 과정 없이 바로 머지할 수 있을 뿐이다.

## 이 프로젝트 적용
- 부트스트랩 때 `docs/bootstrap-requirements`(PR #22)와 `chore/bootstrap-automation`(PR #23)는 둘 다 main의 초기 커밋 `86e8363`에서 갈라졌다.
  - #22는 `docs/` 아래만, #23은 `CLAUDE.md`·`.claude/`·`.github/`·`.gitattributes`만 바꿨다 → **겹치는 파일이 없어서** 순서와 상관없이 충돌 없이 머지됐다.
  - 이렇게 되도록 **처음부터 파일 영역으로 브랜치를 나눴다**(문서 🟡 / 규칙·자동화 🔴 → 검토자와 머지 등급도 달라서 나눈 이유가 하나 더 있음).
- 머지 결과(`git log --graph`): main에 merge commit 2개(`8de7a6a` #22, `be12d10` #23)가 생기고, 각 브랜치의 커밋이 그대로 보존된다(merge commit 방식, `--merge`).
- 앞으로 규칙: **SRS 1개 = 이슈 1개 = PR 1개**. 이슈를 하나씩 순서대로 머지하면 충돌이 거의 없다. 동시에 여러 이슈를 진행하면 `SRS.md`·`traceability.md`·오늘 일지처럼 **공통 문서에서 충돌이 날 수 있다** → 먼저 머지된 뒤 `git merge main`으로 합치고 표의 해당 줄만 고른다.

## 삽질 / 주의점
- 충돌은 "실패"가 아니라 "사람이 골라야 하는 곳"이라는 표시다. GitHub 화면에서 PR에 "This branch has conflicts"가 뜨면 로컬에서 해결하는 편이 안전하다.
- 머지한 브랜치는 원격에서 자동 삭제되도록 설정했다(`delete_branch_on_merge`). 로컬 브랜치는 `git fetch --prune` 후 `git branch -d <브랜치>`로 지운다.

## 참고
- Git 브랜치 기본: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
- GitHub에서 머지 충돌 해결: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/about-merge-conflicts
