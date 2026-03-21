# autoresearch-domino-karpathy

An **algorithmic adaptation** of the ideas in [karpathy/autoresearch](https://github.com/karpathy/autoresearch), aimed at a combinatorial search problem: **finding strong domino packings on finite grids**.

The spirit is the same as the upstream repo:

- keep the repo very small
- keep a fixed harness
- let the agent edit **one file**
- run short experiments
- keep or discard based on measurable improvement

But instead of optimizing `val_bpb` for a language model, this repo optimizes a domino-packing score over a benchmark suite.

## Upstream inspiration

This repo is **inspired by and structurally adapted from** Karpathy's `autoresearch` pattern.
It is not the original training setup and it does not train neural networks.

## Problem

We study domino packing on rectangular boards with optional blocked cells.
A domino covers exactly two orthogonally adjacent free cells.
The goal is to maximize the number of covered cells.

## Repo structure

Only three files matter:

- **`prepare.py`** — fixed benchmark definitions, scoring, and evaluation harness. Do not modify.
- **`train.py`** — the only file the agent edits. Contains the candidate solver/search strategy.
- **`program.md`** — instructions for the autonomous research loop.

## Metric

Each experiment is scored on a fixed benchmark suite under a fixed wall-clock budget.
The harness reports:

- `score` — total covered cells across benchmark boards, higher is better
- `solved_optimal` — how many instances matched the exact optimum
- `runtime_seconds` — total runtime

The primary objective is:

1. maximize `score`
2. then maximize `solved_optimal`
3. then minimize `runtime_seconds`

## Quick start

```bash
uv sync
uv run prepare.py
uv run train.py
```

## Running the agent

Point your coding agent at `program.md` and let it operate in the same keep/discard loop style as the original repo.

## Design philosophy

- one small repo
- one file to mutate
- one fixed evaluation harness
- one simple measurable objective

That makes it a decent fit for agentic algorithm research.

## Future directions

- richer domino-packing instance families
- local search and branch-and-bound hybrids
- SAT / ILP backends
- pattern databases
- decomposition and symmetry handling
