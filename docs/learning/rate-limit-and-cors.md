# rate limit과 CORS

## 핵심 개념

### rate limit (요청 횟수 제한)
- 같은 출처(여기서는 IP)에서 정해진 시간에 보낼 수 있는 요청 수를 제한한다. 로그인에 걸어 두면 **비밀번호를 계속 바꿔 넣는 무차별 대입(brute force)** 을 크게 늦출 수 있다.
- 초과하면 **429 Too Many Requests**를 주고, `Retry-After` 헤더로 언제 다시 시도할지 알린다.
- 카운터를 어디에 두느냐가 중요하다. 메모리에 두면 **서버 프로세스마다 따로** 센다(개발용으로는 충분, 여러 대로 늘리면 Redis 필요).

### CORS (교차 출처 리소스 공유)
- **브라우저**가 지키는 규칙이다. `https://a.com`에서 받은 페이지의 자바스크립트가 `https://b.com`의 API를 부르면, 브라우저가 b의 응답에 `Access-Control-Allow-Origin` 헤더가 있는지 보고 없으면 결과를 감춘다.
- 서버를 지키는 장치가 아니라 **브라우저 안에서 남의 사이트가 내 API를 마음대로 부르지 못하게** 하는 장치다. curl이나 네이티브 앱(Expo Go)에는 적용되지 않는다.
- 쓰기 요청 전에 브라우저가 **preflight**(OPTIONS)로 "이 출처·메서드 허용?"을 먼저 묻는다.

## 이 프로젝트 적용 (SRS-014, 이슈 #9)
- 라이브러리: **slowapi**(Starlette/FastAPI용). 앱을 만들 때 `Limiter`를 새로 만들어 붙인다 → 테스트끼리 카운터가 섞이지 않는다.
- 설정은 환경 변수로만 둔다.
  | 변수 | 기본값 | 용도 |
  |---|---|---|
  | `PUBLIC_RATE_LIMIT` | `30/minute` | `/health` 등 공개 엔드포인트 |
  | `AUTH_RATE_LIMIT` | `5/minute` | `/auth/login`·`/auth/register` (SRS-010·011에서 적용) |
  | `CORS_ORIGINS` | 비어 있음 | 쉼표로 구분한 허용 출처. 비면 CORS 헤더를 아예 안 붙임 |
- 429 응답 본문을 프로젝트 오류 형식 `{"detail": "..."}`으로 맞췄다(arc42 8.3).
- `allow_credentials=False`로 둔다. 토큰을 `Authorization` 헤더로 보내고 쿠키를 쓰지 않기 때문이다. 참고로 **`allow_credentials=True`와 `allow_origins=["*"]`는 함께 쓸 수 없다**(FastAPI 문서).
- 코드: `backend/app/infrastructure/rate_limit.py`, `config.py`, `main.py`

## 삽질 / 주의점
- slowapi에서 `headers_enabled=True`를 쓰면 엔드포인트가 **`request`와 `response` 인자를 모두** 받아야 한다. 없으면 `parameter 'response' must be an instance of starlette.responses.Response` 오류가 난다.
- 라우터를 모듈 최상단에서 만들면 앱마다 다른 Limiter를 붙일 수 없다 → `create_health_router(limiter, limit)`처럼 **팩토리 함수**로 만들었다.
- rate limit은 IP 기준이라 공유기·프록시 뒤에서는 여러 사람이 한 IP로 묶인다. 배포 때 프록시를 쓰면 `X-Forwarded-For` 처리를 다시 봐야 한다.
- CORS는 브라우저 전용이므로, **CORS를 막았다고 API가 보호되는 것은 아니다.** 인증·인가가 따로 필요하다.

## 참고
- FastAPI CORS: https://fastapi.tiangolo.com/tutorial/cors/
- slowapi: https://pypi.org/project/slowapi/
- MDN CORS: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
