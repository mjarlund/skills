# CadQuery

Read this when the chosen tool is CadQuery.

## Install

```bash
pip install cadquery          # or: conda install -c conda-forge cadquery
```

Install into the project's virtualenv if it has one. Wheels lag new Python
releases; if pip fails, use a Python version CadQuery lists as supported.

## File layout

```python
# models/part_name.py — one-line description of the part
import sys
import cadquery as cq

# Size (mm)
W, D, H = 60, 40, 25
WALL = 2.0
# Fit (mm)
FIT = 0.2         # slip clearance per side
HOLE_COMP = 0.2   # added to vertical hole diameters

# Open-top box on Z=0: shelling with the top face selected removes that face.
result = (
    cq.Workplane("XY")
    .box(W, D, H, centered=(True, True, False))
    .faces(">Z").shell(-WALL)
)

if __name__ == "__main__":
    solid = result.val()
    assert solid.isValid(), "invalid solid"
    bb = solid.BoundingBox()
    print(f"size: {bb.xlen:.2f} x {bb.ylen:.2f} x {bb.zlen:.2f} mm")
    out = sys.argv[1] if len(sys.argv) > 1 else "out/part_name.stl"
    cq.exporters.export(result, out, tolerance=0.01, angularTolerance=0.1)
    cq.exporters.export(result, out.replace(".stl", ".svg"))  # preview projection
```

- Keep every dimension as a named constant at the top.
- `.box()` is centered on all axes by default; `centered=(True, True, False)` puts
  the part on the bed.
- `.shell(-WALL)` with no face selected makes a closed hollow solid — almost never
  what a printed part needs. Select the face to remove first.
- `tolerance` controls STL facet size; 0.01 mm keeps holes round enough to fit.

## Common operations

```python
# Holes are cut from a workplane on a face
r = r.faces(">Z").workplane()
r = r.pushPoints([(20, 12), (-20, 12), (20, -12), (-20, -12)]).hole(3.4 + HOLE_COMP)
r = r.faces(">Z").workplane().cboreHole(3.4, 6.2, 3.3)   # Ø, counterbore Ø, depth
r = r.faces(">Z").workplane().cskHole(3.4, 7.0, 90)      # Ø, countersink Ø, angle

# Add a feature on a face (it fuses with the body)
r = r.faces(">Z").workplane().rect(10, 10).extrude(5)

# Edges
r = r.edges("|Z").fillet(1.5)    # vertical edges
r = r.edges("<Z").chamfer(0.5)   # bottom edges: hides elephant's foot
```

Fillet and chamfer last — they fail on edges that later operations change, and
OCC errors like `BRep_API: command not done` usually mean the radius is larger than
the geometry around the edge allows.

## Build, check, preview

```bash
python models/part_name.py out/part_name.stl
python3 <skill-dir>/scripts/check_stl.py out/part_name.stl --expect 60x40x25
```

The SVG is a line drawing with hidden edges dashed. To look at it as an image,
convert it if a converter exists (`rsvg-convert -o out/part.png out/part.svg`, or
`cairosvg out/part.svg -o out/part.png`); otherwise rely on the size check and describe the geometry
from the code.

## Testing that parts fit together

Move one part along the path it takes and check the overlap volume at each pose; touching
faces give about 0.

```python
def overlap(a, b):
    common = a.intersect(b).vals()
    return sum(v.Volume() for v in common) if common else 0.0

for dy in (20, 12, 6, 3, 0):                      # key sliding toward its slot
    assert overlap(cradle, key.translate((0, dy, 0))) < 0.5, f"collides at dy={dy}"
```

Also check the finished pose is clear, and that pulling the part the wrong way collides
if it is meant to hold.
