# Using the official Frontier-CS algorithmic stack

This repo is structured for autoresearch now, but the **official** Problem 0 judge still depends on the Frontier-CS algorithmic stack.

## Current state

- local repo: ready for Karpathy-style iteration
- official Frontier-CS repo: cloned separately in the workspace at `../Frontier-CS`
- blocker on this host: Docker is not installed yet

## Once Docker is installed

From the Frontier-CS repo:

```bash
cd ../Frontier-CS/algorithmic

docker compose up --build -d
curl http://localhost:8081/problems
```

Then from this repo, you can evaluate a generated C++ solver against the official judge via the Frontier-CS CLI / Python API.

## Practical integration plan

1. Keep doing rapid heuristic iteration in this repo.
2. Once Docker is available, add a bridge script that:
   - renders/export a C++ submission candidate
   - calls the official Frontier-CS evaluator for problem 0
   - records score into `results.tsv`
3. Promote changes only when they improve judged score.

## Why this split exists

The current Python harness is intentionally tiny and inspectable.
The official Frontier-CS algorithmic stack is the source of truth for judged results.

Use this repo for:
- autoresearch workflow
- iteration discipline
- logging and branch management

Use the official stack for:
- real Problem 0 evaluation
- checker-backed validation
- leaderboard-comparable scoring
