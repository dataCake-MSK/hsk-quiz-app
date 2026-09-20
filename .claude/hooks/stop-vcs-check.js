// Stop hook: blocks Claude from ending a turn while version-control or daily-journal work is left undone.
const { execSync } = require('child_process');
const fs = require('fs');

const cwd = process.env.CLAUDE_PROJECT_DIR || process.cwd();

let input = {};
try {
  input = JSON.parse(fs.readFileSync(0, 'utf8') || '{}');
} catch {}
// Second pass after a block: let Claude stop so it can't loop forever.
if (input.stop_hook_active) process.exit(0);

const git = (args) => {
  try {
    return execSync(`git ${args}`, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }).trim();
  } catch {
    return null;
  }
};

if (git('rev-parse --is-inside-work-tree') !== 'true') process.exit(0);

const problems = [];

const dirty = (git('status --porcelain') || '').split('\n').filter(Boolean);
if (dirty.length) {
  const shown = dirty.slice(0, 8).map((l) => `  ${l}`).join('\n');
  const more = dirty.length > 8 ? `\n  …외 ${dirty.length - 8}개` : '';
  problems.push(`커밋되지 않은 변경 ${dirty.length}개:\n${shown}${more}`);
}

const branch = git('rev-parse --abbrev-ref HEAD');
if (branch && branch !== 'HEAD') {
  if (branch === 'main') {
    const ahead = Number(git('rev-list --count origin/main..main') || 0);
    if (ahead > 0) problems.push(`main에 push되지 않은 로컬 커밋 ${ahead}개 (main 직접 push 금지 → 브랜치로 옮겨 PR)`);
  } else {
    const upstream = git('rev-parse --abbrev-ref --symbolic-full-name @{u}');
    const ahead = upstream
      ? Number(git('rev-list --count @{u}..HEAD') || 0)
      : Number(git('rev-list --count origin/main..HEAD') || 0);
    if (ahead > 0) problems.push(`브랜치 ${branch}에 push되지 않은 커밋 ${ahead}개`);
  }
}

// 비밀 값 스캔: 커밋되기 전에 작업 트리에서 걸러낸다 (공개 저장소).
const SECRET_PATTERNS = [
  [/\bgh[pousr]_[A-Za-z0-9]{20,}/, 'GitHub 토큰'],
  [/\bgithub_pat_[A-Za-z0-9_]{20,}/, 'GitHub PAT'],
  [/\bsk-[A-Za-z0-9]{20,}/, 'API 키(sk-)'],
  [/\bAKIA[0-9A-Z]{16}\b/, 'AWS 액세스 키'],
  [/-----BEGIN [A-Z ]*PRIVATE KEY-----/, '개인 키'],
  [/\bpostgres(?:ql)?(?:\+\w+)?:\/\/[^\s:/@]+:[^\s@]+@/, 'DB 접속 문자열(비밀번호 포함)'],
  [/\b(?:JWT_SECRET|SECRET_KEY|API_KEY|PASSWORD)\s*[:=]\s*["']?[^\s"'<>$#]{8,}/i, '설정 파일의 비밀 값'],
  [/https:\/\/[a-z0-9-]+\.trycloudflare\.com/, '터널 주소(개인 URL)'],
  [/\b[a-z0-9-]+\.exp\.direct\b/, 'Expo 터널 주소(개인 URL)'],
];

const scanTargets = () => {
  const out = [];
  const diff = [git('diff -U0'), git('diff --cached -U0')].filter(Boolean).join('\n');
  if (diff) out.push(['변경분(diff)', diff]);
  const untracked = (git('ls-files --others --exclude-standard') || '').split('\n').filter(Boolean);
  for (const file of untracked.slice(0, 200)) {
    try {
      if (fs.statSync(file).size > 512 * 1024) continue;
      out.push([file, fs.readFileSync(file, 'utf8')]);
    } catch {}
  }
  return out;
};

const secretHits = [];
for (const [where, text] of scanTargets()) {
  for (const [pattern, label] of SECRET_PATTERNS) {
    if (pattern.test(text)) secretHits.push(`${label} 의심 — ${where}`);
  }
}
if (secretHits.length) {
  problems.push(
    `비밀 값·개인 URL 의심 (커밋 금지, 확인 필요):\n${[...new Set(secretHits)].map((h) => `  ${h}`).join('\n')}`,
  );
}

const now = new Date();
const pad = (n) => String(n).padStart(2, '0');
const today = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
const journal = `docs/journal/${today}.md`;
const lastWork = Number(
  git(`log -1 --all --no-merges --since="${today}T00:00:00" --format=%ct -- . ":(exclude)docs/journal"`) || 0,
);
if (lastWork) {
  const lastJournal = Number(git(`log -1 --all --format=%ct -- "${journal}"`) || 0);
  const journalDirty = dirty.some((l) => l.includes(journal));
  if (lastJournal < lastWork && !journalDirty) {
    problems.push(`오늘 커밋된 작업이 일간 일지(${journal})에 반영되지 않음`);
  }
}

if (!problems.length) process.exit(0);

const reason = [
  '[형상관리 점검] 턴을 끝내기 전에 처리할 항목이 있습니다.',
  ...problems.map((p) => `- ${p}`),
  '',
  '처리 방법 (CLAUDE.md "자동 형상관리" 규칙):',
  '0. 비밀 값·개인 URL 의심이면 커밋하지 말고 값을 .env로 옮기거나 문서에서 지운 뒤 사용자에게 알린다.',
  '1. 일지 누락이면 journal 스킬로 오늘 일지를 갱신한다.',
  '2. 이번 작업에서 사용자가 새로 알게 된 개념·시행착오가 있으면 learn 스킬로 기록한다.',
  '3. commit 스킬로 브랜치 → 커밋 → push → PR, 머지 등급에 따라 자체 머지 또는 사용자 머지 대기.',
  '4. 변경이 사용자가 직접 작업 중인 파일 등 이번 작업과 무관해 보이면 커밋하지 말고 사용자에게 알린다.',
].join('\n');

process.stdout.write(JSON.stringify({ decision: 'block', reason }));
