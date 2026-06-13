---
name: 3d-print
description: Generate 3D-printable parts as CadQuery Python scripts that export STL files. Use when user wants to design, model, or create a 3D-printable object, part, enclosure, mount, bracket, or STL file. Triggers: "3d print", "STL", "print a", "design a part", "CadQuery", "FDM", "printable".
---

# 3D Print Skill

## Quick start

```bash
pip install cadquery
```

Generate Python script → run to produce `.stl` → slice in PrusaSlicer/Cura → print.

## Workflow

### 1. Gather requirements
Ask before writing any code:
- What does it do / hold / attach to?
- Key dimensions (or look up standard specs — MagSafe, VESA, M3 bolt, etc.)
- Material: PLA / PETG / TPU?
- Print orientation preference?
- Any clearances needed (snap-fit, sliding, loose)?

### 2. Three-checkpoint build

**Checkpoint A — Base shape**: Generate outer body only, no features. Show code + describe shape. Get approval.

**Checkpoint B — Features**: Add holes, slots, clips, channels. Re-run self-review checklist. Get approval.

**Checkpoint C — Finish**: Fillets, chamfers, branding text, material-specific tweaks. Final STL export.

### 3. Self-review checklist (run before each checkpoint)
- [ ] Bottom face flat (bed adhesion)
- [ ] Overhangs ≤ 45° (no supports needed)
- [ ] Wall thickness ≥ 1.2 mm (2 mm default)
- [ ] Bridge spans ≤ 20 mm
- [ ] Hole clearances: +0.3 mm for PLA, +0.4 mm for PETG, +0.5 mm for TPU
- [ ] No zero-thickness or coincident faces

## CadQuery patterns

### Basic part + STL export
```python
import cadquery as cq

result = (
    cq.Workplane("XY")
    .box(40, 30, 10)
    .edges("|Z").fillet(2)
    .faces(">Z").hole(6.3)  # M6 clearance
)

result.val().exportStl("part.stl", tolerance=0.01, angularTolerance=0.1)
```

### Parametric with variables
```python
W, D, H = 40, 30, 10
WALL = 2.0
HOLE_D = 3.3 + 0.3  # M3 clearance + PLA tolerance

body = (
    cq.Workplane("XY")
    .box(W, D, H)
    .shell(-WALL)  # hollow
)
```

### Common fastener clearances (PLA)
| Fastener | Clearance drill |
|----------|----------------|
| M2       | 2.4 mm         |
| M3       | 3.3 mm         |
| M4       | 4.3 mm         |
| M5       | 5.3 mm         |

## Design defaults
- Wall: 2.0 mm
- Fillet: 1.5 mm (exterior corners)
- Chamfer bottom edge: 0.5 mm (improves bed adhesion)
- Layer height assumed: 0.2 mm (round Z dims to multiples)
- STL tolerance: `tolerance=0.01, angularTolerance=0.1`

## Iterative refinement
Accept natural language corrections:
- "make it 5mm taller" → adjust `H` variable
- "thicker walls" → bump `WALL` from 2 to 3
- "looser fit" → increase clearance by +0.2 mm
- ASCII sketch → interpret geometry, confirm before building

## STL export snippet (always include)
```python
cq.exporters.export(result, "output.stl", exportType="STL",
                    tolerance=0.01, angularTolerance=0.1)
```

## See also
- [REFERENCE.md](REFERENCE.md) — standard part dimensions, material properties, slicer settings
