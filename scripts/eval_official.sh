#!/usr/bin/env bash
set -euo pipefail

# Placeholder for official Frontier-CS judge evaluation.
# Requires Docker + Frontier-CS algorithmic judge stack to be running.

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 path/to/solution.cpp" >&2
  exit 1
fi

SOLUTION_PATH="$1"
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

cat <<EOF
Official evaluation placeholder
-----------------------------
Solution:    $SOLUTION_PATH
Frontier-CS: $FRONTIER_DIR
Judge URL:   $JUDGE_URL

Expected future flow once Docker is installed:
  cd "$FRONTIER_DIR/algorithmic"
  docker compose up --build -d
  cd "$FRONTIER_DIR"
  uv run frontier eval algorithmic 0 "$SOLUTION_PATH" --judge-url "$JUDGE_URL"
EOF
