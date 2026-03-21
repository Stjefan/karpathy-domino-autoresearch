# EXPERIMENT_PROTOCOL.md

This file is for coding-agent / harness driven autoresearch.

## Mission

Improve Frontier-CS Algorithmic Problem 0 packing quality by changing only `train.py`.

## Current branch

Use the active research branch, typically:

```bash
autoresearch/mar21-p0
```

## Files of record

- `train.py` — the only mutable experiment file
- `prepare.py` — fixed local harness, do not modify during a run
- `results.tsv` — untracked experiment ledger
- `run.log` — latest run output
- `STATUS.md` — current summary and next likely ideas

## Baseline workflow

1. Read `README.md`, `AGENTS.md`, `program.md`, `STATUS.md`.
2. Inspect current `results.tsv`.
3. Make exactly one focused change in `train.py`.
4. Commit the change.
5. Run evaluation.
6. Compare score against baseline/current best.
7. Keep only if improved materially, or tied while simpler/faster.
8. Otherwise reset/discard.

## Local evaluation command

```bash
uv run train.py > run.log 2>&1
```

## Future official evaluation command

Once Docker + Frontier-CS judge are available, use:

```bash
bash scripts/eval_official.sh path/to/solution.cpp
```

## Keep/discard rule

Prefer this priority:

1. higher score
2. same score with lower runtime
3. same score with simpler code

## Constraints

- Do not add dependencies.
- Do not change `prepare.py` during an experiment cycle.
- Do not silently redefine the score.
- Keep diffs small and reviewable.

## Notes

This repo is intentionally small so agent loops stay legible.
