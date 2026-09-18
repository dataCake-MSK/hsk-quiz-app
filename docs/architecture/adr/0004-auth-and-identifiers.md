# ADR-0004 인증(JWT·Argon2)·인가(소유자 필터·admin 역할)·식별자 전략

- 상태: 제안
- 날짜: 2026-09-17
- 관련: NB-002, NB-013, NB-015, SRS-004, SRS-010~014, SRS-023

## 맥락
- 앱(Expo)이 API를 호출하므로 쿠키 세션보다 토큰 인증이 맞다.
- 공용 데이터(HSK 단어, 카테고리, 공용 혼동 관계)와 유저 소유 데이터(커스텀 단어, 즐겨찾기, 숙련도, 세션)가 한 DB에 섞인다. 한 유저가 공용 데이터를 바꾸면 모든 유저에게 영향을 준다.
- ID가 연속 숫자면 남의 리소스 ID를 추측해 호출하는 IDOR 공격이 쉬워진다.

## 결정
- **인증**
  - `POST /auth/login` → access token(15분) + refresh token(14일), JWT HS256, 라이브러리 **PyJWT**
  - 토큰 클레임: `sub`(user_id), `type`(access/refresh), `exp`. `type`이 맞지 않으면 거부
  - 비밀번호: **pwdlib + Argon2** (FastAPI 공식 튜토리얼 권장)
  - `JWT_SECRET`은 환경 변수. 없으면 서버 시작 실패
  - 앱은 토큰을 `expo-secure-store`에 저장
- **인가**
  - `users.role` = `user` | `admin`. 공용 데이터 변경(공용 단어 카테고리, 공용 혼동 관계, 시드)은 admin만
  - 유저 소유 리소스는 모든 조회에 `user_id = :me` 조건. SRS-025부터는 Repository 메서드의 **필수 인자**로 강제
  - 단어 조회 범위: `owner_id IS NULL OR owner_id = :me`. 혼동 관계: `added_by IS NULL OR added_by = :me`
  - 남의 리소스는 **403이 아니라 404**로 응답(존재 여부를 알려주지 않음). 역할 부족은 403
- **식별자**
  - 내부 PK는 `BIGINT GENERATED ALWAYS AS IDENTITY`
  - IDOR은 ID를 숨겨서가 아니라 **소유자 필터로** 막는다. 모든 유저 소유 API에 "다른 유저 토큰 → 404" 테스트를 둔다
- **그 밖**: 로그인·가입 rate limit, CORS 허용 출처를 환경 변수로, 배포 시 HTTPS 강제(배포 단계에서 결정)

## 대안
| 대안 | 선택하지 않은 이유 |
|---|---|
| 외부에 노출하는 ID를 UUID(v4/v7)로 | 추측은 어려워지지만 인가 누락을 가리는 효과만 있음. 학습 초기에는 BIGINT로 조인·인덱스를 단순하게. 배포 전 재검토 |
| bcrypt (passlib) | passlib 유지보수가 멈춤. FastAPI 문서가 pwdlib+Argon2로 바뀜 |
| 유저 태깅도 모두에게 공유(원안) | 인가 규칙이 느슨해지고 공용 데이터가 오염됨 |
| refresh token DB 저장·rotation | 1차 범위 밖(NB-018). 로그아웃은 앱에서 토큰 삭제 |

## 결과
- 좋아지는 점: 역할·소유자 규칙이 명확하고 테스트로 확인 가능
- 감수하는 점: refresh token을 서버에서 무효화할 수 없음(탈취 시 만료까지 유효)
- 재검토 조건: 실제 배포 전, 유저가 본인 외로 늘어날 때
