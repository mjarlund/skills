# 3D Print Reference

## Standard dimensions

### Screw holes (clearance, PLA +0.3 mm)
| Screw | Thread | Clearance | Head dia | Head depth |
|-------|--------|-----------|----------|------------|
| M2    | 2.0    | 2.4       | 4.5      | 1.5        |
| M3    | 3.0    | 3.3       | 6.0      | 2.0        |
| M4    | 4.0    | 4.3       | 8.0      | 2.5        |
| M5    | 5.0    | 5.3       | 9.5      | 3.0        |
| M6    | 6.0    | 6.3       | 11.5     | 3.5        |

### Heat-set inserts (M3, most common)
- OD: 4.5 mm, depth: 5.7 mm
- Bore in part: 4.2 mm (PLA shrink-fit)

### Common consumer device specs
| Device          | Key dim          |
|-----------------|-----------------|
| MagSafe puck    | 56 mm dia        |
| VESA 75         | 75×75 mm holes   |
| VESA 100        | 100×100 mm holes |
| USB-A port      | 14×6.5 mm cutout |
| USB-C port      | 9×3.5 mm cutout  |
| Raspberry Pi 4  | 85×56 mm, M2.5 holes at 3.5/61.5 × 3.5/52.5 |

## Material tolerances (add to clearance holes)
| Material | Shrink offset |
|----------|---------------|
| PLA      | +0.3 mm       |
| PETG     | +0.4 mm       |
| TPU 95A  | +0.5 mm       |
| ABS      | +0.5 mm       |

## FDM constraints
| Constraint        | Limit    | Notes                          |
|-------------------|----------|--------------------------------|
| Min wall          | 1.2 mm   | 2 mm recommended               |
| Min feature       | 0.8 mm   | smaller may not print          |
| Overhang angle    | ≤ 45°    | beyond needs support           |
| Bridge length     | ≤ 20 mm  | longer needs support           |
| Min hole dia      | 2.0 mm   | smaller drills poorly          |
| Layer height      | 0.2 mm   | round Z dims to multiple       |

## Snap-fit clearance
- Cantilever deflection gap: 0.3–0.5 mm
- Latch undercut: 0.5–1.0 mm
- Snap-fit wall thickness: ≥ 1.5 mm

## Slicer recommendations
- Perimeters/walls: 3 (matches 2 mm wall at 0.4 mm nozzle × 3 × 2 passes)
- Top/bottom layers: 4
- Infill: 20% gyroid for general use, 40%+ for load-bearing
- Support: tree supports, 45° threshold, 0.2 mm z-distance

## CadQuery install
```bash
pip install cadquery
# or with conda:
conda install -c conda-forge cadquery
```

## Useful CadQuery operations
```python
# Shell (hollow box)
.shell(-2.0)

# Counterbore hole (screw head recess)
.cboreHole(3.3, 6.0, 2.5)   # drill, cbore_dia, cbore_depth

# Countersink
.cskHole(3.3, 6.0, 82)       # drill, csk_dia, csk_angle

# Pattern of holes
.pushPoints([(10,10), (-10,10), (10,-10), (-10,-10)])
.hole(3.3)

# Extrude from face
.faces(">Z").workplane()
.rect(10, 10).extrude(5)

# Chamfer bottom edges (bed adhesion)
.edges("<Z").chamfer(0.5)
```
