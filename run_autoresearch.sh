#!/usr/bin/env bash
set -euo pipefail

# Lightweight Karpathy-style autoresearch loop driver.
# Safe default: single baseline/eval run unless LOOP=1 is exported.

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

RESULTS_FILE="results.tsv"
LOG_FILE="run.log"

if [[ ! -f "$RESULTS_FILE" ]]; then
  printf 'commit\tscore\tvalid_cases\truntime_seconds\tstatus\tdescription\n' > "$RESULTS_FILE"
fi

run_once() {
  uv run train.py > "$LOG_FILE" 2>&1
  local score valid runtime status commit
  score="$(grep '^score:' "$LOG_FILE" | awk '{print $2}')"
  valid="$(grep '^valid_cases:' "$LOG_FILE" | awk '{print $2}')"
  runtime="$(grep '^runtime_seconds:' "$LOG_FILE" | awk '{print $2}')"
  status="$(grep '^status:' "$LOG_FILE" | awk '{print $2}')"
  commit="$(git rev-parse --short HEAD)"
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$commit" "$score" "$valid" "$runtime" "$status" "manual-or-baseline run" >> "$RESULTS_FILE"
  cat "$LOG_FILE"
}

run_once

if [[ "${LOOP:-0}" != "1" ]]; then
  echo
  echo 'LOOP disabled. Export LOOP=1 only when you want a persistent autoresearch loop.'
  exit 0
fi

while true; do
  echo 'Autoresearch loop placeholder: edit train.py, commit, rerun, compare, keep/discard.'
  sleep 30
  run_once
  break
done
