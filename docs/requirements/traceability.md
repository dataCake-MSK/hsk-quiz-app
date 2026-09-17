# 추적표 (Traceability)

NB → PRD → SRS → 이슈 → PR 연결. PR을 만들거나 머지할 때 AI가 갱신한다.

- 상태: `todo` → `in-progress`(PR 열림) → `done`(머지) / `planned`(2·3차, 이슈 미등록)

| NB | PRD | SRS | 이슈 | PR | 상태 |
|---|---|---|---|---|---|
| - | 기반 | SRS-001 백엔드 스캐폴딩 | - | - | todo |
| NB-017 | 기반 | SRS-002 Expo 스캐폴딩 | - | - | todo |
| - | 기반 | SRS-003 CI | - | - | todo |
| NB-002 | PRD-001 | SRS-004 PostgreSQL·users | - | - | todo |
| NB-002 | PRD-001 | SRS-010 회원가입 API | - | - | todo |
| NB-002 | PRD-001 | SRS-011 로그인·내 정보 | - | - | todo |
| NB-002 | PRD-001 | SRS-012 토큰 갱신 | - | - | todo |
| NB-002 | PRD-001 | SRS-013 앱 가입·로그인 화면 | - | - | todo |
| NB-013 | PRD-001 | SRS-014 rate limit·CORS | - | - | todo |
| NB-003 | PRD-002 | SRS-020 단어 테이블·목록 API | - | - | todo |
| NB-003, NB-004 | PRD-002, PRD-003 | SRS-021 앱 단어 목록·상세 | - | - | todo |
| NB-003 | PRD-002 | SRS-022 커스텀 단어 | - | - | todo |
| NB-004, NB-015 | PRD-003 | SRS-023 카테고리 | - | - | todo |
| NB-005 | PRD-004 | SRS-024 즐겨찾기 | - | - | todo |
| NB-012 | PRD-004 | SRS-025 Repository 도입 | - | - | todo |
| NB-001 | PRD-005 | SRS-030 혼동 관계·세션 시작 | - | - | todo |
| NB-001 | PRD-005 | SRS-031 다음 문제 | - | - | todo |
| NB-001 | PRD-005 | SRS-032 답변·숙련도 | - | - | todo |
| NB-001 | PRD-005 | SRS-033 세션 종료·결과 | - | - | todo |
| NB-005, NB-012 | PRD-004, PRD-005 | SRS-034 즐겨찾기 퀴즈·Strategy | - | - | todo |
| NB-012 | PRD-005 | SRS-035 뜻→단어·Factory | - | - | todo |
| NB-006 | PRD-006 | SRS-040 수동 혼동 태깅 | - | - | planned |
| NB-007 | PRD-007 | SRS-041 오답노트 | - | - | planned |
| NB-008 | PRD-008 | SRS-042 학습 통계 | - | - | planned |
| NB-009 | PRD-009 | SRS-050 타임어택 | - | - | planned |
| NB-010 | PRD-010 | SRS-051 던전 모드 | - | - | planned |

## 보류·미승격 NB
| NB | 상태 | 다음 행동 |
|---|---|---|
| NB-016 HSK 기준·데이터 출처 | hold | SRS-020 착수 전 리포트로 결정 |
| NB-018 토큰 rotation·비밀번호 재설정·2FA | hold | 1차 이후 검토 |

## ADR
| ADR | 관련 |
|---|---|
| [ADR-0001](../architecture/adr/0001-fastapi-expo-monorepo.md) | SRS-001, SRS-002 |
| [ADR-0002](../architecture/adr/0002-postgresql-sqlalchemy-alembic.md) | SRS-004 |
| [ADR-0003](../architecture/adr/0003-clean-architecture-layers.md) | SRS-001, SRS-025 |
| [ADR-0004](../architecture/adr/0004-auth-and-identifiers.md) | SRS-004, SRS-010~014 |
