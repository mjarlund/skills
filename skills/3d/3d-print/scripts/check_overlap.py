#!/usr/bin/env python3
"""Check that two OpenSCAD parts do (or do not) collide in a given pose.

Use it to test an ASSEMBLY, not just a finished shape: a key that sits correctly in
its slot can still be impossible to push in. Run it at several poses along the path
the parts take (start, mid-way, final) and check the clearances you rely on.

Usage:
    check_overlap.py model.scad "cradle()" "translate([0, 12, 0]) key()"
    check_overlap.py model.scad "A" "B" -D tol=0.2 --max-volume 0.5

A and B are OpenSCAD expressions that call modules from model.scad (the file is
pulled in with `use`, so its own top-level geometry is not drawn). Variables in the
file are not visible; pass what you need as literals or with -D.

Exit 0 = no collision (touching faces are not a collision), 1 = collision,
2 = could not run. Needs openscad on PATH; otherwise stdlib only.
"""

import argparse
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_stl  # noqa: E402


def overlap_volume(model, expr_a, expr_b, defines):
    if not os.path.isfile(model):
        raise RuntimeError(f"model file not found: {model}")
    with tempfile.TemporaryDirectory() as tmp:
        scad = os.path.join(tmp, "overlap.scad")
        stl = os.path.join(tmp, "overlap.stl")
        with open(scad, "w") as f:
            f.write(f"use <{os.path.abspath(model)}>\n")
            f.write(f"intersection() {{ {expr_a}; {expr_b}; }}\n")
        cmd = ["openscad", "-o", stl]
        for d in defines:
            cmd += ["-D", d]
        run = subprocess.run(cmd + [scad], capture_output=True, text=True)
        text = run.stdout + run.stderr
        # A misspelled module is silently ignored and looks like "no collision": fail instead.
        for bad in ("Ignoring unknown module", "Ignoring unknown function", "Can't open", "Parser error"):
            if bad.lower() in text.lower():
                raise RuntimeError(text.strip())
        if "empty" in text.lower() and not os.path.exists(stl):
            return 0.0                               # empty intersection: no overlap
        if run.returncode != 0 or not os.path.exists(stl):
            raise RuntimeError(text.strip() or "openscad failed")
        try:
            return abs(check_stl.analyse(check_stl.load_stl(stl))["volume"])
        except ValueError:
            return 0.0                               # degenerate sheet from face contact


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("model")
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("-D", action="append", default=[], dest="defines", metavar="NAME=VALUE")
    ap.add_argument("--max-volume", type=float, default=0.5,
                    help="overlap in mm3 still treated as touching (default 0.5)")
    args = ap.parse_args()
    try:
        vol = overlap_volume(args.model, args.a, args.b, args.defines)
    except (OSError, RuntimeError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    collide = vol > args.max_volume
    print(f"overlap: {vol:.2f} mm3  ->  {'COLLISION' if collide else 'clear'}")
    return 1 if collide else 0


if __name__ == "__main__":
    sys.exit(main())
