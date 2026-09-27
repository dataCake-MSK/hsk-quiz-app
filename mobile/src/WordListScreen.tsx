import { useEffect, useState } from "react";
import { ActivityIndicator, FlatList, Pressable, StyleSheet, Text, View } from "react-native";

import { ApiError, fetchWords, type HskLevel, type Word } from "./api";

const LEVELS: HskLevel[] = [1, 2, 3];

/** 어떤 급수·몇 번째 시도의 결과인지 함께 담는다. 지금 보고 있는 조건과 다르면 "불러오는 중"이다. */
type Result = {
  level: HskLevel;
  attempt: number;
  words?: Word[];
  error?: string;
};

type Props = {
  onSelect: (word: Word) => void;
};

export default function WordListScreen({ onSelect }: Props) {
  const [level, setLevel] = useState<HskLevel>(1);
  const [attempt, setAttempt] = useState(0);
  const [result, setResult] = useState<Result | null>(null);

  useEffect(() => {
    // 탭을 빠르게 바꿨을 때 늦게 도착한 응답이 화면을 덮어쓰지 않도록 한다.
    let cancelled = false;

    const run = async () => {
      try {
        const words = await fetchWords(level);
        if (!cancelled) setResult({ level, attempt, words });
      } catch (error) {
        const message = error instanceof ApiError ? error.message : "단어를 불러오지 못했습니다";
        if (!cancelled) setResult({ level, attempt, error: message });
      }
    };

    void run();
    return () => {
      cancelled = true;
    };
  }, [level, attempt]);

  // 결과가 없거나, 지금 고른 조건의 결과가 아직 아니면 로딩 중.
  const isLoading = result === null || result.level !== level || result.attempt !== attempt;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>단어</Text>

      <View style={styles.tabs}>
        {LEVELS.map((value) => (
          <Pressable
            key={value}
            accessibilityRole="button"
            style={[styles.tab, value === level && styles.tabActive]}
            onPress={() => setLevel(value)}
          >
            <Text style={[styles.tabText, value === level && styles.tabTextActive]}>
              {value}급
            </Text>
          </Pressable>
        ))}
      </View>

      {isLoading && (
        <View style={styles.center}>
          <ActivityIndicator />
          <Text style={styles.muted}>불러오는 중…</Text>
        </View>
      )}

      {!isLoading && result.error && (
        <View style={styles.center}>
          <Text style={styles.error}>{result.error}</Text>
          <Pressable
            accessibilityRole="button"
            style={styles.retry}
            onPress={() => setAttempt((value) => value + 1)}
          >
            <Text style={styles.retryText}>다시 시도</Text>
          </Pressable>
        </View>
      )}

      {!isLoading && result.words?.length === 0 && (
        <View style={styles.center}>
          <Text style={styles.muted}>단어가 없습니다</Text>
        </View>
      )}

      {!isLoading && result.words && result.words.length > 0 && (
        <FlatList
          data={result.words}
          keyExtractor={(word) => String(word.word_id)}
          renderItem={({ item }) => (
            <Pressable style={styles.row} onPress={() => onSelect(item)}>
              <Text style={styles.hanzi}>{item.hanzi}</Text>
              <View style={styles.rowBody}>
                <Text style={styles.pinyin}>
                  {item.pinyin} · {item.kr_pronunciation}
                </Text>
                <Text style={styles.meaning}>{item.meaning_kr}</Text>
              </View>
            </Pressable>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, paddingHorizontal: 16 },
  title: { fontSize: 24, fontWeight: "600", marginBottom: 12 },
  tabs: { flexDirection: "row", gap: 8, marginBottom: 12 },
  tab: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    backgroundColor: "#eef1f5",
  },
  tabActive: { backgroundColor: "#1d76db" },
  tabText: { fontSize: 15, color: "#333" },
  tabTextActive: { color: "#fff", fontWeight: "600" },
  center: { flex: 1, alignItems: "center", justifyContent: "center", gap: 12 },
  muted: { color: "#666", fontSize: 15 },
  error: { color: "#b60205", fontSize: 15, textAlign: "center" },
  retry: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    backgroundColor: "#1d76db",
  },
  retryText: { color: "#fff" },
  row: {
    flexDirection: "row",
    alignItems: "center",
    gap: 14,
    paddingVertical: 12,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: "#dcdfe4",
  },
  hanzi: { fontSize: 28, width: 64 },
  rowBody: { flex: 1, gap: 2 },
  pinyin: { fontSize: 14, color: "#555" },
  meaning: { fontSize: 16 },
});
