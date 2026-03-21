"""
Fixed local harness for Frontier-CS Algorithmic Problem 0 style polyomino packing.
Do not modify during autoresearch.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import time

Cell = tuple[int, int]
Piece = tuple[Cell, ...]
Placement = tuple[int, int, int, int]  # X, Y, R, F


@dataclass(frozen=True)
class Case:
    name: str
    pieces: tuple[Piece, ...]


def normalize(piece: list[Cell] | tuple[Cell, ...]) -> Piece:
    min_x = min(x for x, _ in piece)
    min_y = min(y for _, y in piece)
    return tuple(sorted((x - min_x, y - min_y) for x, y in piece))


def transform_cell(cell: Cell, r: int, f: int) -> Cell:
    x, y = cell
    if f:
        x = -x
    r %= 4
    if r == 0:
        return x, y
    if r == 1:
        return y, -x
    if r == 2:
        return -x, -y
    return -y, x


def transform_piece(piece: Piece, r: int, f: int) -> Piece:
    return normalize([transform_cell(c, r, f) for c in piece])


def unique_transforms(piece: Piece) -> list[tuple[Piece, int, int]]:
    seen = set()
    out = []
    for f in (0, 1):
        for r in range(4):
            p = transform_piece(piece, r, f)
            if p not in seen:
                seen.add(p)
                out.append((p, r, f))
    return out


def piece_area(piece: Piece) -> int:
    return len(piece)


def bounding_box(piece: Piece) -> tuple[int, int]:
    w = max(x for x, _ in piece) + 1
    h = max(y for _, y in piece) + 1
    return w, h


def cases() -> list[Case]:
    mono = ((0, 0),)
    domino = ((0, 0), (1, 0))
    tri_i = ((0, 0), (1, 0), (2, 0))
    tri_l = ((0, 0), (0, 1), (1, 0))
    tet_o = ((0, 0), (1, 0), (0, 1), (1, 1))
    tet_i = ((0, 0), (1, 0), (2, 0), (3, 0))
    tet_t = ((0, 0), (1, 0), (2, 0), (1, 1))
    tet_l = ((0, 0), (0, 1), (0, 2), (1, 0))
    tet_s = ((0, 0), (1, 0), (1, 1), (2, 1))
    pent_p = ((0, 0), (1, 0), (0, 1), (1, 1), (0, 2))
    pent_u = ((0, 0), (0, 1), (1, 1), (2, 1), (2, 0))
    pent_f = ((1, 0), (0, 1), (1, 1), (1, 2), (2, 2))

    library = [mono, domino, tri_i, tri_l, tet_o, tet_i, tet_t, tet_l, tet_s, pent_p, pent_u, pent_f]
    return [
        Case("tiny_mix", tuple(library[:8] * 2)),
        Case("medium_mix", tuple(library * 3)),
        Case("tetra_heavy", tuple([tet_o, tet_i, tet_t, tet_l, tet_s] * 8)),
        Case("penta_mix", tuple([pent_p, pent_u, pent_f, tet_t, tri_l, domino] * 8)),
        Case("large_mix", tuple(library * 8)),
    ]


def apply_placement(piece: Piece, placement: Placement) -> list[Cell]:
    x0, y0, r, f = placement
    transformed = transform_piece(piece, r, f)
    return [(x + x0, y + y0) for x, y in transformed]


def evaluate_solver(solver) -> dict:
    started = time.perf_counter()
    total_score = 0.0
    valid_cases = 0
    case_results = []

    for case in cases():
        W, H, placements = solver(case.pieces)
        ok = True
        if not isinstance(W, int) or not isinstance(H, int) or W <= 0 or H <= 0:
            ok = False
        if len(placements) != len(case.pieces):
            ok = False

        occupied: set[Cell] = set()
        total_cells = sum(len(p) for p in case.pieces)
        if ok:
            for piece, placement in zip(case.pieces, placements):
                cells = apply_placement(piece, placement)
                for x, y in cells:
                    if not (0 <= x < W and 0 <= y < H):
                        ok = False
                        break
                    if (x, y) in occupied:
                        ok = False
                        break
                    occupied.add((x, y))
                if not ok:
                    break

        area = W * H if isinstance(W, int) and isinstance(H, int) and W > 0 and H > 0 else 10**18
        score = (1e5 * total_cells / area) if ok else 0.0
        total_score += score
        if ok:
            valid_cases += 1
        case_results.append({
            "name": case.name,
            "score": score,
            "area": area,
            "valid": ok,
            "n_pieces": len(case.pieces),
            "total_cells": total_cells,
        })

    runtime = time.perf_counter() - started
    return {
        "score": total_score,
        "valid_cases": f"{valid_cases}/{len(cases())}",
        "runtime_seconds": runtime,
        "status": "success",
        "cases": case_results,
    }


if __name__ == "__main__":
    print(json.dumps({"cases": [c.name for c in cases()]}, indent=2))
