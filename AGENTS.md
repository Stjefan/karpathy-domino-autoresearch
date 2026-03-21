# AGENTS.md

Repo purpose: run Karpathy-style autoresearch for Frontier-CS Algorithmic Problem 0.

## Files that matter

- `prepare.py` — fixed local harness, do not modify during a research run
- `train.py` — the single mutable file for packing strategy experiments
- `program.md` — human/agent loop instructions
- `results.tsv` — untracked experiment ledger
- `run_autoresearch.sh` — small helper to run and log baseline/manual experiments

## Rules

- prefer small, testable changes
- preserve validity first
- only keep changes that improve score, or tie while simplifying/runtime-improving
- log every run
- do not silently alter the metric

## Current reality

- the local Python harness is a fast scaffold
- the official Frontier-CS judge should become the final evaluator once Docker is available on the host
