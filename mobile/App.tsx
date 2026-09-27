import { StatusBar } from "expo-status-bar";
import { useEffect, useState } from "react";
import { SafeAreaView, StyleSheet, Text } from "react-native";

import { fetchHealth, type Word } from "./src/api";
import WordDetailScreen from "./src/WordDetailScreen";
import WordListScreen from "./src/WordListScreen";

export default function App() {
  const [selected, setSelected] = useState<Word | null>(null);
  const [serverNote, setServerNote] = useState<string | null>(null);

  // 화면 하단에 서버 상태를 한 줄로 둔다(문제가 생겼을 때 원인을 바로 알기 위해).
  useEffect(() => {
    let cancelled = false;
    fetchHealth()
      .then((health) => {
        if (!cancelled) setServerNote(`서버 ${health.status} · DB ${health.db}`);
      })
      .catch((error: Error) => {
        if (!cancelled) setServerNote(error.message);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <SafeAreaView style={styles.safe}>
      {selected ? (
        <WordDetailScreen word={selected} onBack={() => setSelected(null)} />
      ) : (
        <WordListScreen onSelect={setSelected} />
      )}

      {serverNote && <Text style={styles.note}>{serverNote}</Text>}
      <StatusBar style="auto" />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#fff", paddingTop: 48 },
  note: { fontSize: 12, color: "#888", textAlign: "center", paddingVertical: 6 },
});
