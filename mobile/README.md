# mobile — HSK Quiz 앱

Expo(SDK 57) + React Native + TypeScript. 폰의 Expo Go로 확인한다.

## 실행
```bash
cd mobile
npm install
cp .env.example .env        # EXPO_PUBLIC_API_URL 채우기
npx expo start --tunnel --go
npx tsc --noEmit            # 타입 검사
```

- `--tunnel`: 인터넷만 되면 어디서든 접속(내부적으로 `@expo/ngrok` 사용). 같은 Wi‑Fi면 `--tunnel` 없이도 된다.
- PC와 폰의 Expo Go가 같은 Expo 계정으로 로그인되어 있으면 Expo Go 홈의 개발 서버 목록에 뜬다.

## 백엔드 연결
- 앱은 `EXPO_PUBLIC_API_URL`의 `/health`를 호출해 첫 화면에 상태를 보여준다.
- 폰과 PC가 다른 네트워크면 **백엔드도 따로 공개 주소가 필요하다**. 방법은 [리포트](../docs/reports/2026-09-20-phone-backend-access.md) 참고.
- `EXPO_PUBLIC_` 값은 앱 번들에 그대로 들어가므로 비밀 값을 넣지 않는다.
