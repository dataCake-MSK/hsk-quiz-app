import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";

import type { Word } from "./api";

type Props = {
  word: Word;
  onBack: () => void;
};

export default function WordDetailScreen({ word, onBack }: Props) {
  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Pressable accessibilityRole="button" onPress={onBack} style={styles.back}>
        <Text style={styles.backText}>← 목록</Text>
      </Pressable>

      <Text style={styles.hanzi}>{word.hanzi}</Text>
      <Text style={styles.pinyin}>{word.pinyin}</Text>
      <Text style={styles.kr}>한국어 발음: {word.kr_pronunciation}</Text>

      <View style={styles.block}>
        <Text style={styles.meaning}>{word.meaning_kr}</Text>
        <Text style={styles.muted}>
          {word.pos ? `${word.pos} · ` : ""}HSK {word.hsk_level}급
        </Text>
      </View>

      {word.example_sentence && (
        <View style={styles.block}>
          <Text style={styles.label}>예문</Text>
          <Text style={styles.example}>{word.example_sentence}</Text>
          {word.example_meaning_kr && (
            <Text style={styles.muted}>{word.example_meaning_kr}</Text>
          )}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16, gap: 8 },
  back: { paddingVertical: 8 },
  backText: { fontSize: 16, color: "#1d76db" },
  hanzi: { fontSize: 64, textAlign: "center" },
  pinyin: { fontSize: 22, textAlign: "center", color: "#444" },
  kr: { fontSize: 16, textAlign: "center", color: "#666", marginBottom: 8 },
  block: {
    gap: 4,
    paddingVertical: 12,
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: "#dcdfe4",
  },
  label: { fontSize: 13, color: "#888" },
  meaning: { fontSize: 20, fontWeight: "600" },
  example: { fontSize: 18, lineHeight: 26 },
  muted: { fontSize: 15, color: "#666" },
});
