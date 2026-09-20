# 리포트: 폰에서 앱과 백엔드에 접속하는 방식

- 작성: 2026-09-20
- 상태: 확정 (SRS-002에서 실제로 동작 확인)
- 관련: NB-017, SRS-002(이슈 #2), ADR-0001

## 1. 요약
- 사용자는 **PC와 다른 네트워크에 있을 때가 많다** → 기본은 **터널 방식**.
- 터널이 **2개** 필요하다. 앱 화면(Metro)과 백엔드 API는 서로 다른 프로세스이기 때문이다.
  | 무엇 | 도구 | 명령 |
  |---|---|---|
  | 앱 화면(Metro, 8081) | `@expo/ngrok` (프로젝트 개발 의존성) | `npx expo start --tunnel --go` |
  | 백엔드 API(8000) | `cloudflared` 빠른 터널(계정 불필요) | `cloudflared tunnel --url http://localhost:8000` |
- 앱은 백엔드 주소를 `mobile/.env`의 `EXPO_PUBLIC_API_URL`에서 읽는다. **터널 주소는 실행할 때마다 바뀌므로 켤 때마다 `.env`를 갱신**하고 Expo를 다시 시작한다.

## 2. 왜 이 조합인가
| 방식 | 되는 조건 | 판단 |
|---|---|---|
| 같은 Wi‑Fi LAN IP (`http://<PC IP>:8000`) | PC와 폰이 같은 네트워크, 방화벽 허용 | 집에서는 가장 빠르지만 밖에서는 불가 → 보조 |
| **cloudflared 빠른 터널** | 인터넷만 되면 됨, 계정 불필요 | **채택**. `winget install --id Cloudflare.cloudflared`로 설치(사용자 범위) |
| ngrok | 계정·authtoken 필요 | 백엔드용으로는 가입이 필요해 보류. Metro용으로는 Expo가 내장해 사용 중 |

- 옆 저장소 `D_personal-api-app`은 백엔드가 없어 Metro 터널만 썼다. 그 방식(`@expo/ngrok` + `--tunnel --go`)은 그대로 차용하고, 백엔드 터널만 새로 정했다.

## 3. 실행 순서 (Claude가 수행)
```bash
# 1) 백엔드
cd backend && uv run fastapi dev app/main.py --port 8000

# 2) 백엔드 터널 → 출력된 https://<랜덤>.trycloudflare.com 주소 확인
cloudflared tunnel --url http://localhost:8000 --no-autoupdate

# 3) 앱 환경 변수 갱신 (.env는 커밋하지 않음)
#    mobile/.env → EXPO_PUBLIC_API_URL=https://<랜덤>.trycloudflare.com

# 4) 앱 개발 서버 (8081이 사용 중이면 --port 8082)
cd mobile && npx expo start --tunnel --go
```
- 백그라운드로 실행하면 터미널에 QR·주소가 안 나온다. **Expo 주소는 ngrok 로컬 API**에서 얻는다.
  ```bash
  curl -s http://127.0.0.1:4040/api/tunnels     # 다른 Expo가 떠 있으면 4041, 4042…
  ```
  `public_url`(https)을 `exp://`로 바꿔 사용자에게 전달한다. 폰 Expo Go에서 그 링크를 열거나, PC와 같은 Expo 계정으로 로그인해 개발 서버 목록에서 연다.

## 4. 주의점
| 주제 | 내용 |
|---|---|
| 주소 수명 | cloudflared 빠른 터널 주소는 **실행할 때마다 바뀐다**. `.env` 갱신 후 Expo 재시작 필요 |
| 포트 충돌 | 다른 프로젝트의 Expo가 8081을 쓰면 `--port 8082`. ngrok 검사 API도 4040 → 4041로 밀린다 |
| 보안 | 터널이 켜져 있는 동안 **로컬 API가 인터넷에 공개**된다. 인증이 붙기 전(SRS-010~014)까지는 확인이 끝나면 바로 끈다 |
| 비밀 값 | 터널 주소는 개인 URL로 취급해 **코드·문서·커밋·일지에 쓰지 않는다**(채팅으로만 전달). `EXPO_PUBLIC_` 값은 앱 번들에 그대로 들어가므로 비밀 값 금지 |
| 서버 관리 | 개발 서버·터널은 확인이 끝났거나 약 30분이 지나면 계속 켤지 사용자에게 묻는다(CLAUDE.md) |

## 5. 결정 필요
- 없음. NB-017은 이 리포트로 해결(상태 `promoted` → 적용).

## 참고
- Expo CLI `--tunnel`: https://docs.expo.dev/more/expo-cli/
- Expo 환경 변수(`EXPO_PUBLIC_`는 번들에 노출): https://docs.expo.dev/guides/environment-variables/
- Cloudflare 빠른 터널: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/
