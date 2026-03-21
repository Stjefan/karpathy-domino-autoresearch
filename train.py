"""
Editable solver file for autoresearch-domino-karpathy.
Usage: uv run train.py
"""

from __future__ import annotations

from collections import deque

from prepare import evaluate_solver

Cell = tuple[int, int]
Domino = tuple[Cell, Cell]


def _neighbors(width: int, height: int, blocked: frozenset[Cell], cell: Cell) -> list[Cell]:
    x, y = cell
    out = []
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nxt = (x + dx, y + dy)
        if 0 <= nxt[0] < width and 0 <= nxt[1] < height and nxt not in blocked:
            out.append(nxt)
    return out


def solve(width: int, height: int, blocked: frozenset[Cell]) -> list[Domino]:
    # Baseline exact solver via bipartite maximum matching.
    import networkx as nx

    free = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if (x, y) not in blocked
    ]
    left = [c for c in free if (c[0] + c[1]) % 2 == 0]

    graph = nx.Graph()
    graph.add_nodes_from(left, bipartite=0)
    graph.add_nodes_from([c for c in free if c not in left], bipartite=1)

    for cell in left:
        for nxt in _neighbors(width, height, blocked, cell):
            if (nxt[0] + nxt[1]) % 2 == 1:
                graph.add_edge(cell, nxt)

    matching = nx.algorithms.bipartite.matching.maximum_matching(graph, top_nodes=set(left))
    packing: list[Domino] = []
    used = set()
    for a in left:
        b = matching.get(a)
        if b is None or a in used or b in used:
            continue
        packing.append((a, b))
        used.add(a)
        used.add(b)
    return packing


if __name__ == "__main__":
    result = evaluate_solver(solve)
    print("---")
    print(f"score:            {result['score']}")
    print(f"solved_optimal:   {result['solved_optimal']}")
    print(f"runtime_seconds:  {result['runtime_seconds']:.4f}")
    print(f"budget_seconds:   {result['budget_seconds']:.2f}")
    print(f"status:           {result['status']}")
