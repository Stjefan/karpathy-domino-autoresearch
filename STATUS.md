# STATUS.md

## Current objective

Use a Karpathy-style autoresearch loop to improve packing quality for Frontier-CS Algorithmic Problem 0.

## Current best known local baseline

- branch: `autoresearch/mar21-p0`
- baseline commit: `c95cb78`
- workflow setup commit: `77be847`
- score: `366859.161793`
- valid cases: `5/5`
- runtime: `~0.02s`

## Current solver

A valid but simple heuristic:
- enumerate unique transforms
- choose compact orientation greedily
- sort pieces by rough difficulty/size
- shelf-pack across candidate widths
- keep the best `(area, H, W)`

## Biggest current weakness

It is still basically a shelf packer.
That means it wastes space badly on awkward polyomino mixes.

## Good next experiments

1. skyline placement instead of simple shelves
2. width-search strategy informed by total cell count / bbox statistics
3. better orientation scoring with placement-awareness
4. local repacking of the worst shelf
5. shape-family specific ordering heuristics

## Official evaluation status

- Frontier-CS repo cloned in workspace at `../Frontier-CS`
- official Docker judge is now running locally
- `http://localhost:8081/problems` responds
- end-to-end `frontier eval algorithmic 0 ...` has been verified
- next step is to improve judged C++ submissions, not just the local Python scaffold
- current official baseline submission: `solutions/problem0_baseline.cpp`
- current official judged score: `0.00`
