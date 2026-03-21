# karpathy-domino-autoresearch

A **Karpathy-style autoresearch adaptation** for **Frontier-CS Algorithmic Problem 0**.

The exact problem is **not domino matching**. It is:

> Pack many small polyominoes into an axis-aligned rectangle, allowing translation, rotation, and reflection, while minimizing the rectangle area.

This repo keeps the spirit of `karpathy/autoresearch`:

- tiny repo
- fixed harness in `prepare.py`
- one editable file: `train.py`
- a `program.md` that defines the autonomous improvement loop

## Problem summary

Input: many polyominoes, each with 1–10 cells.

Output:
- rectangle width `W` and height `H`
- one transform per polyomino:
  - translation `(X, Y)`
  - rotation `R ∈ {0,1,2,3}`
  - reflection flag `F ∈ {0,1}`

Goal:
- minimize rectangle area `A = W * H`
- ties prefer smaller `H`, then smaller `W`

## This repo's purpose

This is a **research scaffold**, not an exact clone of the official Frontier-CS evaluation stack.
It is designed to let an agent iterate on packing strategies in the Karpathy keep/discard style.

## Repo structure

Only three files matter:

- `prepare.py` — fixed benchmark cases, transforms, validation, scoring
- `train.py` — the only file to mutate during autoresearch
- `program.md` — instructions for autonomous experimentation

## Metric

For the local harness, higher is better:

- `score = 1e5 * total_cells / total_area_sum`

Tie-break intuition:
- smaller total area is better
- more valid packings is better
- lower runtime is better

## Quick start

```bash
uv sync
uv run prepare.py
uv run train.py
```

## Baseline

The current baseline is intentionally simple:

- enumerate unique transforms for each piece
- choose a compact orientation greedily
- place pieces using a shelf-style rectangle packing heuristic

That is a **valid starting point**, not a strong solver.

## Good next research directions

- better ordering of pieces
- skyline / guillotine style placement
- local improvement after initial placement
- width search and restart strategies
- component-specific rules by polyomino shape family
- lower bounds for pruning
- hybrid exact search on small subinstances
