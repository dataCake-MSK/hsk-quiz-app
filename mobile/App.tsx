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
      return { kind: "error", message: `서버 응답 오류 (${response.status})` };
    }
    const body = (await response.json()) as { status?: string };
    return { kind: "ok", status: body.status ?? "unknown" };
  } catch {
    return { kind: "error", message: "서버에 연결할 수 없음" };
  }
}

export default function App() {
  const [status, setStatus] = useState<Status>({ kind: "loading" });

  const check = useCallback(() => {
    setStatus({ kind: "loading" });
    void fetchHealth().then(setStatus);
  }, []);

  useEffect(check, [check]);

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
