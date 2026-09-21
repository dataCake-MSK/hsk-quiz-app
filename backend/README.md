# backend — HSK Quiz API

FastAPI 서버. 패키지 관리는 [uv](https://docs.astral.sh/uv/).

## 실행
```bash
cd backend
uv sync                                          # 의존성 설치 (.venv 생성)
cp .env.example .env                             # DATABASE_URL 등 채우기 (커밋되지 않음)
uv run --env-file .env alembic upgrade head      # DB 스키마 적용
uv run --env-file .env fastapi dev app/main.py   # http://127.0.0.1:8000 , 문서 /docs
uv run --env-file .env pytest                    # 테스트 (DB 테스트 포함)
uv run pytest                                    # DB 없이 (DB 테스트는 건너뜀)
uv run ruff check .                              # lint
```

- `.env`는 자동으로 읽히지 않는다. `uv run --env-file .env` 로 넘긴다.
- `GET /health` → `{"status":"ok","db":"ok"}`. `db`는 `ok` / `unavailable`(연결 실패) / `not_configured`(DATABASE_URL 없음).

## 구조 (클린 아키텍처 4계층, ADR-0003)
| 폴더 | 계층 | import 가능 |
|---|---|---|
| `app/domain/` | 엔티티, 순수 규칙 | 표준 라이브러리만 |
| `app/application/` | 유스케이스, `ports/` | domain |
| `app/interface/` | 라우터(`routers/`), DTO | application, domain |
| `app/infrastructure/` | DB, 보안, 설정 | 모두 |

지금은 `GET /health`만 있다. Repository·Strategy·Factory 패턴은 아직 필요하지 않아 넣지 않았다(도입 시점: SRS-025, 034, 035).
