# autoresearch-domino-karpathy

This is an algorithmic adaptation of the autoresearch loop.

## Setup

To set up a new experiment, work with the user to:

1. **Agree on a run tag**: propose a tag based on today's date. The branch `autoresearch/<tag>` must not already exist.
2. **Create the branch**: `git checkout -b autoresearch/<tag>` from current master.
3. **Read the in-scope files**:
   - `README.md`
   - `prepare.py` — fixed benchmark harness, do not modify
   - `train.py` — the file you modify
4. **Verify setup**: run `uv run prepare.py` once if needed.
5. **Initialize results.tsv**: create it with only the header row.
6. **Confirm and go**.

## Experimentation

Each experiment runs with a fixed benchmark suite and fixed wall-clock budget.
You launch it as:

```bash
uv run train.py
```

**What you CAN do:**
- Modify `train.py` only.
- Change solver logic, heuristics, search ordering, pruning, decomposition, data structures, and internal strategy.

**What you CANNOT do:**
- Modify `prepare.py`.
- Install new packages or add dependencies.
- Modify the benchmark suite or scoring logic.

## Goal

The goal is to maximize `score` reported by the harness.
Tie-breakers:
1. more `solved_optimal`
2. lower runtime

## First run

The very first run should always establish the baseline.
Run the training script as-is before making changes.

## Output format

When the script finishes it prints a summary like this:

```text
---
score:            412
solved_optimal:   12/12
runtime_seconds:  0.14
budget_seconds:   5.00
status:           success
```

## Logging results

When an experiment is done, log it to `results.tsv` (tab-separated).

Header:

```text
commit	score	solved_optimal	runtime_seconds	status	description
```

Example:

```text
commit	score	solved_optimal	runtime_seconds	status	description
a1b2c3d	412	12/12	0.14	keep	baseline exact matcher
b2c3d4e	412	12/12	0.09	keep	component splitting
c3d4e5f	404	10/12	0.04	discard	too-greedy heuristic
```

## Experiment loop

LOOP FOREVER:

1. Look at current branch/commit.
2. Edit `train.py` with one experimental idea.
3. git commit.
4. Run `uv run train.py > run.log 2>&1`.
5. Extract results from `run.log`.
6. If the run crashes, inspect the traceback and decide whether to fix or discard.
7. Record the result in `results.tsv` (leave it untracked).
8. If the score improved, keep the commit.
9. If the score is worse, or tie-breakers are worse, reset back.

**Timeout**: if a run exceeds 10 minutes, kill it and treat it as failure.

**Simplicity criterion**: all else equal, simpler is better.

**Never stop** once the loop begins, unless manually interrupted by the human.
