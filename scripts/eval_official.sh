#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 path/to/solution.cpp" >&2
  exit 1
fi

SOLUTION_PATH="$1"
if [[ "$SOLUTION_PATH" != /* ]]; then
  SOLUTION_PATH="$(cd "$(dirname "$SOLUTION_PATH")" && pwd)/$(basename "$SOLUTION_PATH")"
fi
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FRONTIER_DIR="${FRONTIER_DIR:-$REPO_DIR/../Frontier-CS}"
JUDGE_URL="${JUDGE_URL:-http://localhost:8081}"

if [[ ! -f "$SOLUTION_PATH" ]]; then
  echo "Solution file not found: $SOLUTION_PATH" >&2
  exit 1
fi
if [[ ! -d "$FRONTIER_DIR" ]]; then
  echo "Frontier-CS repo not found at: $FRONTIER_DIR" >&2
  exit 1
fi

TMP_LOG="$(mktemp)"
trap 'rm -f "$TMP_LOG"' EXIT

(
  cd "$FRONTIER_DIR"
  uv run frontier eval algorithmic 0 "$SOLUTION_PATH" --judge-url "$JUDGE_URL"
) | tee "$TMP_LOG"

SCORE="$(grep -Eo 'Score: [0-9]+(\.[0-9]+)?' "$TMP_LOG" | tail -n1 | awk '{print $2}')"
if [[ -n "${SCORE:-}" ]]; then
  echo "OFFICIAL_SCORE=$SCORE"
fi
