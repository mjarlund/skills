#!/usr/bin/env python3
"""Check an exported STL against what a printable part needs.

Usage:
    check_stl.py part.stl
    check_stl.py part.stl --expect 60x40x25 [--tol 0.5] [--allow-shells N]

Reports size, volume, shell count, bed contact, and mesh defects.
Exit 0 = pass (warnings are advisory), 1 = errors found, 2 = bad input.

Units: STL has none; coordinates are read as millimetres.
Not checked: wall thickness, overhang angles, bridges, self-intersection.
Stdlib only, so it runs anywhere python3 does.
"""

import argparse
import math
import struct
import sys
from collections import defaultdict

WELD = 1e-4       # mm; vertices closer than this are the same vertex
BED_EPS = 0.01    # mm; faces this close to min Z count as touching the bed


def load_stl(path):
    with open(path, "rb") as f:
        data = f.read()
    if len(data) >= 84:
        count = struct.unpack_from("<I", data, 80)[0]
        if 84 + count * 50 == len(data):
            tris = []
            for off in range(84, len(data), 50):
                v = struct.unpack_from("<12f", data, off)
                tris.append((v[3:6], v[6:9], v[9:12]))
            return tris
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("not a valid binary or ASCII STL")
    tris, cur = [], []
    for line in text.splitlines():
        parts = line.split()
        if parts and parts[0] == "vertex" and len(parts) == 4:
            cur.append(tuple(float(p) for p in parts[1:]))
            if len(cur) == 3:
                tris.append(tuple(cur))
                cur = []
    if not tris:
        raise ValueError("no triangles found")
    return tris


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def analyse(tris):
    index, verts, faces = {}, [], []

    def vid(p):
        key = tuple(round(c / WELD) for c in p)
        if key not in index:
            index[key] = len(verts)
            verts.append(p)
        return index[key]

    degenerate = 0
    for tri in tris:
        if any(not math.isfinite(c) for p in tri for c in p):
            raise ValueError("non-finite vertex coordinates")
        f = tuple(vid(p) for p in tri)
        if len(set(f)) < 3:
            degenerate += 1
            continue
        faces.append(f)

    # Edge use: undirected count finds holes / non-manifold edges;
    # directed count finds inconsistent winding (flipped faces).
    undirected = defaultdict(list)
    directed = defaultdict(int)
    for fi, (a, b, c) in enumerate(faces):
        for u, v in ((a, b), (b, c), (c, a)):
            undirected[frozenset((u, v))].append(fi)
            directed[(u, v)] += 1
    open_edges = sum(1 for fs in undirected.values() if len(fs) == 1)
    nonmanifold = sum(1 for fs in undirected.values() if len(fs) > 2)
    # Only judge winding on clean 2-face edges; non-manifold edges are reported above.
    flipped = sum(1 for (u, v), n in directed.items()
                  if n > 1 and len(undirected[frozenset((u, v))]) == 2)

    # Shells: faces connected through shared edges.
    parent = list(range(len(faces)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for fs in undirected.values():
        for other in fs[1:]:
            ra, rb = find(fs[0]), find(other)
            if ra != rb:
                parent[ra] = rb
    shells = len({find(i) for i in range(len(faces))})

    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]
    zmin = min(zs)

    volume = 0.0
    bed_area = 0.0
    for a, b, c in faces:
        pa, pb, pc = verts[a], verts[b], verts[c]
        volume += (pa[0] * (pb[1] * pc[2] - pb[2] * pc[1])
                   - pa[1] * (pb[0] * pc[2] - pb[2] * pc[0])
                   + pa[2] * (pb[0] * pc[1] - pb[1] * pc[0])) / 6.0
        if all(abs(p[2] - zmin) < BED_EPS for p in (pa, pb, pc)):
            n = cross(sub(pb, pa), sub(pc, pa))
            bed_area += math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2) / 2.0

    return {
        "triangles": len(tris),
        "degenerate": degenerate,
        "open_edges": open_edges,
        "nonmanifold_edges": nonmanifold,
        "flipped_edges": flipped,
        "shells": shells,
        "min": (min(xs), min(ys), zmin),
        "size": (max(xs) - min(xs), max(ys) - min(ys), max(zs) - zmin),
        "volume": volume,
        "bed_area": bed_area,
    }


def parse_expect(s):
    try:
        dims = tuple(float(x) for x in s.lower().split("x"))
    except ValueError:
        dims = ()
    if len(dims) != 3:
        raise argparse.ArgumentTypeError("use WxDxH, e.g. 60x40x25")
    return dims


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("stl")
    ap.add_argument("--expect", type=parse_expect, help="intended size WxDxH in mm")
    ap.add_argument("--tol", type=float, default=0.5, help="size tolerance in mm (default 0.5)")
    ap.add_argument("--allow-shells", type=int, default=1,
                    help="number of separate solids allowed (default 1)")
    args = ap.parse_args()

    try:
        r = analyse(load_stl(args.stl))
    except (OSError, ValueError) as e:
        print(f"ERROR: {args.stl}: {e}", file=sys.stderr)
        return 2

    errors, warnings = [], []
    w, d, h = r["size"]
    print(f"file:      {args.stl}")
    print(f"triangles: {r['triangles']}")
    print(f"size:      {w:.2f} x {d:.2f} x {h:.2f} mm (W x D x H)")
    print(f"min:       {r['min'][0]:.2f}, {r['min'][1]:.2f}, {r['min'][2]:.2f}")
    print(f"volume:    {abs(r['volume']) / 1000:.2f} cm3")
    print(f"shells:    {r['shells']}")
    print(f"bed area:  {r['bed_area']:.1f} mm2")

    if r["open_edges"]:
        errors.append(f"{r['open_edges']} open edges: mesh is not watertight")
    if r["nonmanifold_edges"]:
        errors.append(f"{r['nonmanifold_edges']} non-manifold edges "
                      "(faces touching at an edge, or zero-thickness geometry)")
    if r["flipped_edges"]:
        errors.append(f"{r['flipped_edges']} edges with inconsistent winding (flipped faces)")
    if r["volume"] < 0:
        errors.append("negative volume: normals point inward")
    if abs(r["volume"]) < 1e-6:
        errors.append("zero volume")
    if r["shells"] > args.allow_shells:
        errors.append(f"{r['shells']} separate solids (allowed {args.allow_shells}): "
                      "a feature is floating or only touching at a face/edge")
    if r["degenerate"]:
        warnings.append(f"{r['degenerate']} degenerate triangles dropped")
    if r["bed_area"] < 1.0:
        warnings.append("almost no flat area on the bed at min Z: reorient or add a flat base")
    elif r["bed_area"] < 0.05 * w * d:
        warnings.append("bed contact is under 5% of the footprint: check adhesion / tipping")
    if abs(r["min"][2]) > BED_EPS:
        warnings.append("part does not sit at Z=0 (slicers usually drop it, but check intent)")

    if args.expect:
        for axis, got, want in zip("WDH", r["size"], args.expect):
            if abs(got - want) > args.tol:
                errors.append(f"{axis} is {got:.2f} mm, expected {want:.2f} ±{args.tol}")

    for m in warnings:
        print(f"WARN:  {m}")
    for m in errors:
        print(f"ERROR: {m}")
    print("RESULT: " + ("FAIL" if errors else "PASS"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
