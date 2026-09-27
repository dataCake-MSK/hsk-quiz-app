/** 백엔드 호출을 한곳에 모은다. 주소는 .env의 EXPO_PUBLIC_API_URL에서 읽는다. */

export type Word = {
  word_id: number;
  hanzi: string;
  pinyin: string;
  kr_pronunciation: string;
  meaning_kr: string;
  hsk_level: number;
  pos: string | null;
  example_sentence: string | null;
  example_meaning_kr: string | null;
};

export type HskLevel = 1 | 2 | 3;

const API_URL = process.env.EXPO_PUBLIC_API_URL;

/** 화면에 그대로 보여줄 수 있는 오류. 서버 내부 사정은 담지 않는다. */
export class ApiError extends Error {}

async function request<T>(path: string): Promise<T> {
  if (!API_URL) {
    throw new ApiError("EXPO_PUBLIC_API_URL이 설정되지 않았습니다");
  }

  let response: Response;
  try {
    response = await fetch(`${API_URL}${path}`);
  } catch {
    throw new ApiError("서버에 연결할 수 없음");
  }

  if (!response.ok) {
    // 502·503·504는 터널은 살아 있고 뒤의 서버만 죽은 경우라 연결 실패와 같게 다룬다.
    const unreachable = [502, 503, 504].includes(response.status);
    const message = unreachable ? "서버에 연결할 수 없음" : "서버 응답 오류";
    throw new ApiError(`${message} (${response.status})`);
  }

  return (await response.json()) as T;
}

export function fetchHealth(): Promise<{ status: string; db: string }> {
  return request("/health");
}

export function fetchWords(hskLevel: HskLevel): Promise<Word[]> {
  return request(`/words?hsk_level=${hskLevel}`);
}
