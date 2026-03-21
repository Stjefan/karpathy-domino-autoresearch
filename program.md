# karpathy-domino-autoresearch

This is a Karpathy-style autoresearch loop for **Frontier-CS Algorithmic Problem 0**:
packing many small polyominoes into a small rectangle.

## Setup

1. Choose a run tag like `mar21-p0`.
2. Create a branch: `git checkout -b autoresearch/<tag>`.
3. Read:
   - `README.md`
   - `prepare.py` (fixed harness, do not modify)
   - `train.py` (the only file you modify)
4. Run the baseline once: `bash run_autoresearch.sh`
5. Initialize `results.tsv` with the header row if needed.
6. Record the baseline.

## What you CAN do

- Modify `train.py` only.
- Change piece ordering, orientation selection, placement heuristics, local search, search width selection, and internal data structures.

## What you CANNOT do

- Modify `prepare.py`.
- Add dependencies.
- Change validation or scoring.

## Goal

Maximize `score`.

Practically, that means reducing the rectangle area used by the packer while preserving validity.

## Output format

The script prints a summary like:

```text
---
score:            48372.182318
valid_cases:      12/12
runtime_seconds:  0.0213
status:           success
```

## Logging

Log each experiment to `results.tsv` as tab-separated values:

```text
commit	score	valid_cases	runtime_seconds	status	description
```

## Loop

LOOP FOREVER:

1. inspect current branch/commit
2. make one focused change to `train.py`
3. commit it
4. run `uv run train.py > run.log 2>&1`
5. extract the reported metrics
6. if it crashes, inspect the traceback and either fix or discard
7. append to `results.tsv` (untracked)
8. keep the commit only if score improves materially, or ties while simplifying code / reducing runtime
9. otherwise reset back

## First ideas worth trying

- sort pieces by harder-to-place geometry
- search multiple candidate widths
- skyline placement instead of plain shelves
- bounded local repacking around bad shelves
- maintain occupancy bitsets for faster feasibility tests

## Never stop

Once the experiment loop begins, continue until manually interrupted.
