import { StatusBar } from "expo-status-bar";
import { useCallback, useEffect, useState } from "react";
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from "react-native";

const API_URL = process.env.EXPO_PUBLIC_API_URL;

type Status =
  | { kind: "loading" }
  | { kind: "ok"; status: string }
  | { kind: "error"; message: string };

async function fetchHealth(): Promise<Status> {
  if (!API_URL) {
    return { kind: "error", message: "EXPO_PUBLIC_API_URL이 설정되지 않았습니다" };
  }
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) {
      // 502·503·504는 서버(또는 터널 뒤의 서버)가 떠 있지 않다는 뜻이라 같은 문구로 묶는다.
      // 괄호 안 상태 코드는 개발 중 원인을 구분하기 위한 표시.
      const unreachable = response.status === 502 || response.status === 503 || response.status === 504;
      const message = unreachable ? "서버에 연결할 수 없음" : "서버 응답 오류";
      return { kind: "error", message: `${message} (${response.status})` };
    }
    const body = (await response.json()) as { status?: string };
    return { kind: "ok", status: body.status ?? "unknown" };
  } catch {
    return { kind: "error", message: "서버에 연결할 수 없음" };
  }
}

export default function App() {
  const [status, setStatus] = useState<Status>({ kind: "loading" });

  // 버튼용: 다시 로딩 상태로 되돌린 뒤 조회한다.
  const check = useCallback(() => {
    setStatus({ kind: "loading" });
    void fetchHealth().then(setStatus);
  }, []);

  // 첫 렌더에서 한 번 조회. 화면을 벗어난 뒤 응답이 와도 상태를 바꾸지 않는다.
  useEffect(() => {
    let cancelled = false;
    void fetchHealth().then((result) => {
      if (!cancelled) setStatus(result);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>HSK Quiz</Text>

      {status.kind === "loading" && <ActivityIndicator accessibilityLabel="확인 중" />}
      {status.kind === "ok" && <Text style={styles.ok}>서버 상태: {status.status}</Text>}
      {status.kind === "error" && <Text style={styles.error}>{status.message}</Text>}

      <Pressable style={styles.button} onPress={check}>
        <Text style={styles.buttonText}>다시 확인</Text>
      </Pressable>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "#fff",
    gap: 16,
    padding: 24,
  },
  title: { fontSize: 28, fontWeight: "600" },
  ok: { fontSize: 18, color: "#0e8a16" },
  error: { fontSize: 16, color: "#b60205", textAlign: "center" },
  button: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    backgroundColor: "#1d76db",
  },
  buttonText: { color: "#fff", fontSize: 16 },
});
