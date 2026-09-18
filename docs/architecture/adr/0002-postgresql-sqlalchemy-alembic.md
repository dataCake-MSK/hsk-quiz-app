# ADR-0002 PostgreSQL + SQLAlchemy 2 + Alembic

- 상태: 제안
- 날짜: 2026-09-17
- 관련: SRS-004, SRS-020~035, NB-011

## 맥락
- 학습 목표가 DB 설계(외래키, 자기참조·M:N 정션, CHECK·UNIQUE 제약, 유저별 분리)다. 제약을 DB에서 실제로 걸어보고 확인할 수 있어야 한다.
- 개발 PC(Windows)에 Docker가 없다. 사용자가 PostgreSQL을 직접 설치하기로 했다(2026-09-17).
- SQL Injection을 기본적으로 막기 위해 ORM을 쓰고 raw query는 피한다.

## 결정
- DB: **PostgreSQL** (PC에 직접 설치, `UNIQUE NULLS NOT DISTINCT`를 쓰려면 15 이상)
- ORM: **SQLAlchemy 2** (타입이 있는 `Mapped[...]` 방식), 드라이버 psycopg 3
- 마이그레이션: **Alembic**. 스키마 변경은 항상 마이그레이션 파일로 남긴다
- 접속 정보는 `DATABASE_URL` 환경 변수. 테스트는 `TEST_DATABASE_URL`의 별도 DB

## 대안
| 대안 | 선택하지 않은 이유 |
|---|---|
| SQLite로 시작 | FK를 켜려면 PRAGMA가 필요하고 타입·제약이 달라 나중에 옮기는 작업이 생김 |
| Docker Desktop + PostgreSQL | 설치가 무거움. CI에서는 서비스 컨테이너로 따로 사용 가능 |
| SQLModel | 편하지만 ORM 모델과 도메인 엔티티의 경계가 흐려짐(ADR-0003과 충돌) |
| 관리형 DB(Neon 등) | 외부 서비스 가입·네트워크 의존. 배포 단계에서 검토 |

## 결과
- 좋아지는 점: 배포 환경과 같은 DB로 제약을 직접 확인
- 감수하는 점: 사용자 PC 설치 필요, 로컬 접속 정보는 `.env`로만 관리
- 재검토 조건: 배포 대상 결정 시
