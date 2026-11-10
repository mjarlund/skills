---
name: 3d-print
description: Design 3D-printable parts as parametric CAD scripts (OpenSCAD or CadQuery), verify the geometry, and export STL for slicing. Use whenever the user wants to create or modify a printable part — enclosure, case, mount, bracket, holder, adapter, spacer, knob, clip, lid — or mentions OpenSCAD, .scad files, CadQuery, STL export, or "something I can 3D print", even if they don't say "CAD". For diagnosing a print that already failed, use 3d-diagnose instead.
compatibility: Builds need OpenSCAD or CadQuery (Python). scripts/check_stl.py needs only python3. Without the tools, the skill still writes the model and gives the user exact commands to run.
---

# 3D Print

Turn a description of a physical part into a parametric CAD script that exports a
printable STL, checking at every stage that the geometry is what was intended.

## 1. Requirements

Look first: existing `.scad`/`.py` models, drawings, photos, or datasheets in the
repo often answer the questions below. Then ask only what blocks the base shape —
usually what the part does, what it attaches to or holds, and the critical
dimensions of anything it must fit. Ask one question at a time, with your
recommended answer and why.

For everything else, propose defaults in one short list the user can correct
instead of asking each one:

- Material: PLA (unless heat over ~55 °C, outdoor use, flexing, or repeated snapping)
- Fit: slip, 0.2 mm per side, for mating parts
- Walls: 2.0 mm
- Fasteners: M3, heat-set inserts if it will be opened often
- Print orientation: largest flat face on the bed
- Printer: 0.4 mm nozzle, 0.2 mm layers, bed size not limiting

Dimensions of real objects the part must fit are the biggest source of failed
prints. Ask the user to measure them with calipers when it matters, and list any
dimension you assumed (from a datasheet or REFERENCE.md) so they can check it.

## 2. Tool

Pick without asking, and state the choice and reason in the first checkpoint:

- Existing model in the repo → keep its tool and parameter names.
- OpenSCAD → default: simple to medium geometry, no Python needed, Customizer sliders.
- CadQuery → Python already in the project, fillets on complex edges, STEP output,
  or heavy programmatic generation.

Then read `OPENSCAD.md` or `CADQUERY.md` for file layout, pitfalls, and the build,
check and preview commands.

## 3. Build in checkpoints

- **A. Base body** — overall shape, walls, print orientation. No holes or details.
- **B. Functional features** — holes, fasteners, slots, clips, cable paths, mating
  interfaces.
- **C. Finish** — fillets, chamfers, text, and the final export.

Edit the same script file at each stage. At each checkpoint, verify (below),
review it against the design rules, then show the file path, what changed and why,
and wait for approval. If the user wants it done in one go, run all three without
stopping but still verify each stage.

## 4. Verify every checkpoint

A file that compiles is not a correct part. Wrong sizes, missing cuts, and features
floating free all compile cleanly, and the user only finds out after a print.

1. Export the STL with the tool's command.
2. Check the mesh and size:
   `python3 scripts/check_stl.py <part.stl> --expect WxDxH`
   It fails on holes in the mesh, zero-thickness faces, flipped faces, extra
   solids, and an outer size off by more than 0.5 mm.
3. Render a preview image and look at it. Confirm every feature you added is
   there, in the right place, cut the right way.
4. Fix and repeat before reporting. Report the commands run and their results.

If the CAD tool is not installed, say so plainly, give the exact commands, and do
not describe the part as verified.

## Design rules

These prevent the common printability failures. Values and tables are in
`REFERENCE.md` — read it whenever you size a hole, fastener, fit, insert, snap fit,
or a device cutout.

- **Orientation first.** It decides which overhangs exist and how strong the part
  is: layers pull apart at about half the strength of the plastic along them.
- **Flat base on the bed**, with a 0.4–0.5 mm bottom chamfer so elephant's foot
  doesn't stop the part seating.
- **Overhangs ≤ 45°, bridges ≤ 20 mm.** Use chamfers rather than fillets on
  downward-facing edges, and teardrops for horizontal holes over ~5 mm.
- **Walls 2.0 mm default, 1.2 mm minimum.** Smallest feature about 0.8 mm.
- **Clearance once, per side, on the female feature.** Vertical holes also get
  `HOLE_COMP` because they print undersize.
- **One solid.** Overlap every joined feature into the body; never let parts touch
  only at a face or edge.
- **Z heights in multiples of the layer height** when they matter (lids, steps).

## Fit test piece

When the part has press fits, inserts, or several mating parts, suggest printing
`assets/fit-coupon.scad` once per printer and material (instructions in its
header). It measures that printer's real clearances, hole compensation, and insert
bore, which replace the defaults. Generic values are off by 0.1–0.2 mm between
printers, which is the difference between a press fit and one that won't go in.

## Revisions

Map natural-language changes to parameters, not to new geometry: "5 mm taller" →
`H += 5`; "looser" → raise `FIT`; "holes further out" → hole spacing. If a change
needs a new parameter, add it at the top with the others.

## Deliverable

- Script path and STL path(s), one STL per separately printed part
- Parameter table: name, default, meaning
- The export command and the check result
- Print settings: orientation, material, walls, infill, supports (baseline in
  REFERENCE.md)
- Assumed dimensions the user should check, and what to test on the first print

If a printed part has defects (stringing, warping, layer splits), that is the
`3d-diagnose` skill's job; come back here when the cause turns out to be geometry.
