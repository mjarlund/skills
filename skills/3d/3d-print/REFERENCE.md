# 3D Print Reference

Starting values for FDM with a 0.4 mm nozzle at 0.2 mm layers. They vary by
±0.1–0.2 mm between printers; a fit test piece (`assets/fit-coupon.scad`) printed on
the user's machine overrides every number here.

Contents: Fits · Holes and screws · Nuts · Heat-set inserts · Snap fits ·
FDM limits · Orientation and strength · Materials · Common device dimensions ·
Slicer baseline

## Fits

How to apply: model the bought or male part at its true size, and open the
female/printed feature by the clearance. Values are **per side**; a hole's diameter
grows by 2 × clearance. Apply clearance once — the tables below are nominal sizes
unless they say otherwise.

| Fit | Per side | Use for |
|---|---|---|
| Press | 0.05–0.10 mm | Pins, bearings, magnets that must not come out |
| Snug | 0.10–0.15 mm | Friction lids, caps that hold by friction |
| Slip | 0.20–0.25 mm | Parts that slide or rotate without wobble (default for mating printed parts) |
| Loose | 0.30–0.40 mm | Easy assembly, cable pass-throughs, parts that must drop in |
| Print-in-place | 0.40–0.50 mm | Hinges and joints printed already assembled |

Material adjustments: PETG and TPU ooze more, so add about 0.05 mm per side. ABS
and ASA shrink by 0.5–0.8 %, which matters on parts over about 100 mm. Prefer
loose fits for TPU; it does not hold precise fits.

## Holes and screws

Vertical holes print 0.1–0.3 mm undersize in diameter (faceting, plus the plastic
pulling inward). Add a hole compensation (`HOLE_COMP`, default 0.2 mm on diameter)
to every vertical hole that needs to fit something, or calibrate it with the fit test
piece. Horizontal holes print slightly oval — make them a teardrop (45° pointed roof)
above about 5 mm, or drill them out.

Socket-head cap screws (ISO 4762). Clearance holes already include clearance; add
`HOLE_COMP` only.

| Screw | Clearance hole | Head Ø | Head height | Counterbore Ø × depth | Pilot hole (screw into plastic) |
|---|---|---|---|---|---|
| M2   | 2.4 | 3.8  | 2.0 | 4.4 × 2.3  | 1.6 |
| M2.5 | 2.9 | 4.5  | 2.5 | 5.2 × 2.8  | 2.0 |
| M3   | 3.4 | 5.5  | 3.0 | 6.2 × 3.3  | 2.5 |
| M4   | 4.5 | 7.0  | 4.0 | 7.8 × 4.3  | 3.3 |
| M5   | 5.5 | 8.5  | 5.0 | 9.4 × 5.3  | 4.2 |
| M6   | 6.6 | 10.0 | 6.0 | 11.0 × 6.3 | 5.0 |

Countersunk heads (ISO 10642, 90°): head Ø M3 6.7, M4 9.0, M5 11.2, M6 13.4.
Make the countersink 0.3 mm wider so the head sits flush.

Screwing directly into plastic works for a few assembly cycles. If it will be opened
often, use heat-set inserts or captive nuts.

## Nuts

Hex nuts (ISO 4032). Nut traps: across-flats + 0.2–0.3 mm, depth = height + 0.2 mm.
In OpenSCAD use `cylinder(d = af / cos(30), $fn = 6)`. A trap that opens sideways
prints cleaner than one bridged from below.

| Nut | Across flats | Height |
|---|---|---|
| M2   | 4.0  | 1.6 |
| M2.5 | 5.0  | 2.0 |
| M3   | 5.5  | 2.4 |
| M4   | 7.0  | 3.2 |
| M5   | 8.0  | 4.7 |
| M6   | 10.0 | 5.2 |

## Heat-set inserts

They are melted into the plastic with a soldering iron; they are not a shrink fit.
Bore sizes depend on the insert brand, so follow the vendor's drawing when the user
has one. Typical M3 × 5.7 mm insert: bore 4.0–4.2 mm, bore depth = insert length +
1 mm, at least 1.5–2 mm of plastic around the bore (boss Ø ≥ 8–9 mm). Row C of the fit
test piece finds the right bore. Orient bosses vertically so the insert is pressed
along Z.

## Snap fits

- Cantilever clips: 1.5–2 mm thick at the root, at least 5× as long as the hook is deep,
  root filleted. Print so the clip bends in the XY plane (it snaps along layer lines
  if it bends across them).
- Hook undercut: 0.5–1.0 mm; catch window = hook height + 0.3 mm.
- PLA is brittle and creeps — fine for a few cycles; PETG survives repeated use.

## FDM limits

| Feature | Limit | Notes |
|---|---|---|
| Wall | ≥ 1.2 mm, default 2.0 mm | Thin walls are best as a multiple of line width (≈0.45 mm): 0.9, 1.35, 1.8 |
| Smallest feature | ≈ 0.8 mm | Two line widths; smaller disappears |
| Overhang | ≤ 45° from vertical | Steeper needs support or a chamfer instead of a fillet |
| Bridge | ≤ 20 mm | Longer sags; add support or a pillar |
| Vertical hole | ≥ 2 mm | Smaller: model a pilot and drill |
| Z heights | Multiples of layer height | e.g. a 0.2 mm layer makes 3.1 mm print as 3.0 or 3.2 |
| Bottom edge chamfer | 0.4–0.5 mm × 45° | Hides elephant's foot so parts seat and lids fit |
| Embossed/engraved text | ≥ 0.6 mm deep, ≥ 5 mm tall | Smaller text blurs |

Every joined feature must overlap the body by a small amount (0.01 mm or more).
Faces that only touch produce zero-thickness, non-manifold geometry and separate
solids in the STL.

## Orientation and strength

Choose orientation before modelling details — it decides which overhangs exist.

- Layers bond at roughly half the strength of the plastic along a layer. Orient so
  the main load runs along layers, not pulling them apart.
- Put the largest flat face on the bed. Avoid supports on faces that must fit or seal.
- Strength comes mostly from walls/perimeters, not infill.

## Materials

| Material | Good for | Watch out for |
|---|---|---|
| PLA  | Default: easy, accurate, stiff | Softens around 55–60 °C (cars, sun, near motors); brittle; creeps under constant load |
| PETG | Tougher, outdoor use, mechanical parts | Strings; slightly less accurate; sticks too hard to smooth PEI |
| ABS / ASA | Heat to around 90–100 °C, ASA is UV-stable | Warps — needs an enclosure; fumes |
| TPU 95A | Flexible: gaskets, bumpers, grips | Slow to print, loose tolerances, needs a direct-drive extruder |

## Common device dimensions

Measure the user's actual part with calipers when the fit matters; these are
starting points.

| Device | Dimensions |
|---|---|
| Raspberry Pi 4/5 | Board 85 × 56 mm, M2.5 holes at (3.5, 3.5), (61.5, 3.5), (3.5, 52.5), (61.5, 52.5) |
| VESA 75 / 100 | 75 × 75 / 100 × 100 mm hole square, M4 screws |
| MagSafe charger | Ø 56 mm, about 5.5 mm thick |
| USB-C | Socket opening 9.0 × 3.3 mm; cable plug body up to about 12.5 × 7 mm — size the cutout for the plug if the wall is thicker than about 1.5 mm |
| USB-A | Socket opening 13.5 × 6 mm; cable plug body up to about 16 × 8 mm |

## Slicer baseline

- Walls/perimeters: 3 (about 1.35 mm); 4–6 for load-bearing parts
- Top/bottom: 5 layers at 0.2 mm (1.0 mm)
- Infill: 15–20 % gyroid; 30–40 % for load-bearing parts
- Supports: only where needed, tree/organic, 45–50° threshold, Z gap = one layer
- Brim: 3–5 mm for tall narrow parts, sharp corners, or ABS/ASA
