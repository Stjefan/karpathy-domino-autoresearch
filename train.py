"""
Editable solver file for Karpathy-style polyomino packing autoresearch.
Usage: uv run train.py
"""

from __future__ import annotations

import math

from prepare import Piece, Placement, bounding_box, evaluate_solver, unique_transforms


def best_orientation(piece: Piece) -> tuple[Piece, int, int, int, int]:
    candidates = []
    for transformed, r, f in unique_transforms(piece):
        w, h = bounding_box(transformed)
        candidates.append((w * h, max(w, h), h, w, transformed, r, f))
    _, _, h, w, transformed, r, f = min(candidates)
    return transformed, r, f, w, h


def try_pack(items: list[tuple[int, Piece, int, int, int, int]], width_limit: int) -> tuple[int, int, list[Placement]]:
    x = 0
    y = 0
    shelf_h = 0
    placements_by_index: dict[int, Placement] = {}

    for idx, piece, r, f, w, h in items:
        if x + w > width_limit and x > 0:
            y += shelf_h
            x = 0
            shelf_h = 0
        placements_by_index[idx] = (x, y, r, f)
        x += w
        shelf_h = max(shelf_h, h)
    height = y + shelf_h
    placements = [placements_by_index[i] for i in range(len(items))]
    return width_limit, height, placements


def solve(pieces: tuple[Piece, ...]) -> tuple[int, int, list[Placement]]:
    oriented = [(idx, *best_orientation(piece)) for idx, piece in enumerate(pieces)]
    oriented.sort(key=lambda item: (item[4] * item[5], item[5], item[4], len(item[1])), reverse=True)

    total_bbox_area = sum(w * h for _, _, _, _, w, h in oriented)
    total_cells = sum(len(piece) for _, piece, _, _, _, _ in oriented)
    start_width = max(max(w for _, _, _, _, w, _ in oriented), int(math.sqrt(max(total_cells, total_bbox_area // 2))))

    best = None
    for width in range(start_width, start_width + 16):
        packed = try_pack(oriented, width)
        W, H, placements = packed
        area = W * H
        if best is None or (area, H, W) < (best[0] * best[1], best[1], best[0]):
            best = packed
    assert best is not None
    return best


if __name__ == "__main__":
    result = evaluate_solver(solve)
    print("---")
    print(f"score:            {result['score']:.6f}")
    print(f"valid_cases:      {result['valid_cases']}")
    print(f"runtime_seconds:  {result['runtime_seconds']:.4f}")
    print(f"status:           {result['status']}")
