"""
Fixed benchmark harness for domino-packing autoresearch experiments.
Do not modify this file during the research loop.

Usage:
    uv run prepare.py
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass

Board = tuple[int, int, frozenset[tuple[int, int]]]
TIME_BUDGET = 5.0


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    width: int
    height: int
    blocked: frozenset[tuple[int, int]]

    def board_tuple(self) -> Board:
        return (self.width, self.height, self.blocked)


def _checker_holes(width: int, height: int) -> frozenset[tuple[int, int]]:
    return frozenset(
        (x, y)
        for y in range(height)
        for x in range(width)
        if x % 4 == 1 and y % 4 == 1
    )


def benchmark_suite() -> list[BenchmarkCase]:
    return [
        BenchmarkCase("empty_4x4", 4, 4, frozenset()),
        BenchmarkCase("empty_6x6", 6, 6, frozenset()),
        BenchmarkCase("empty_8x8", 8, 8, frozenset()),
        BenchmarkCase("odd_9x9", 9, 9, frozenset()),
        BenchmarkCase("holes_8x8", 8, 8, _checker_holes(8, 8)),
        BenchmarkCase("holes_12x12", 12, 12, _checker_holes(12, 12)),
        BenchmarkCase("sparse_10x10", 10, 10, frozenset({(1,1),(2,7),(4,4),(5,8),(7,2),(8,8)})),
        BenchmarkCase("frame_12x10", 12, 10, frozenset({(0,5),(11,5),(5,0),(5,9)})),
        BenchmarkCase("cross_11x11", 11, 11, frozenset({(5,y) for y in range(11) if y != 5} | {(x,5) for x in range(11) if x != 5})),
        BenchmarkCase("banded_14x8", 14, 8, frozenset({(x,y) for y in range(8) for x in range(14) if (x+y) % 7 == 0})),
        BenchmarkCase("randomish_12x12", 12, 12, frozenset({(0,0),(1,4),(2,8),(3,3),(4,10),(5,6),(6,1),(7,9),(8,5),(9,11),(10,2),(11,7)})),
        BenchmarkCase("large_16x12", 16, 12, frozenset({(2,2),(3,7),(5,5),(6,9),(8,4),(10,10),(12,3),(13,8)})),
    ]


def exact_optimum(case: BenchmarkCase) -> int:
    import networkx as nx

    free = [
        (x, y)
        for y in range(case.height)
        for x in range(case.width)
        if (x, y) not in case.blocked
    ]
    left = [c for c in free if (c[0] + c[1]) % 2 == 0]
    graph = nx.Graph()
    graph.add_nodes_from(left, bipartite=0)
    graph.add_nodes_from([c for c in free if c not in left], bipartite=1)
    for x, y in left:
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nxt = (x + dx, y + dy)
            if nxt in case.blocked:
                continue
            if 0 <= nxt[0] < case.width and 0 <= nxt[1] < case.height and (nxt[0] + nxt[1]) % 2 == 1:
                graph.add_edge((x, y), nxt)
    matching = nx.algorithms.bipartite.matching.maximum_matching(graph, top_nodes=set(left))
    return sum(1 for c in left if c in matching)


def evaluate_solver(solver) -> dict:
    suite = benchmark_suite()
    started = time.perf_counter()
    results = []
    total_score = 0
    solved_optimal = 0

    for case in suite:
        packing = solver(case.width, case.height, case.blocked)
        used = set()
        valid = True
        for a, b in packing:
            if a in used or b in used:
                valid = False
                break
            ax, ay = a
            bx, by = b
            if abs(ax - bx) + abs(ay - by) != 1:
                valid = False
                break
            for cell in (a, b):
                x, y = cell
                if not (0 <= x < case.width and 0 <= y < case.height):
                    valid = False
                    break
                if cell in case.blocked:
                    valid = False
                    break
            used.add(a)
            used.add(b)
        covered = len(used)
        optimum = exact_optimum(case) * 2
        if valid:
            total_score += covered
            if covered == optimum:
                solved_optimal += 1
        results.append({
            "name": case.name,
            "covered": covered if valid else 0,
            "optimum": optimum,
            "valid": valid,
        })

    runtime = time.perf_counter() - started
    return {
        "score": total_score,
        "solved_optimal": f"{solved_optimal}/{len(suite)}",
        "runtime_seconds": runtime,
        "budget_seconds": TIME_BUDGET,
        "status": "success" if runtime <= TIME_BUDGET else "timeout",
        "cases": results,
    }


if __name__ == "__main__":
    payload = {
        "benchmark_cases": [case.name for case in benchmark_suite()],
        "time_budget_seconds": TIME_BUDGET,
    }
    print(json.dumps(payload, indent=2))
