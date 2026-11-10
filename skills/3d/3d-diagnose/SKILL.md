---
name: 3d-diagnose
description: Diagnose FDM 3D print failures from a text description or photo, rank the likely causes, prescribe slicer and hardware fixes with setting names for Cura, PrusaSlicer, and OrcaSlicer/Bambu Studio, and iterate until resolved. Use whenever the user describes a failed or ugly print, shares a photo of one, asks why a print looks wrong, or mentions stringing, warping, layer splits, under-extrusion, layer shifts, ringing, clogs, elephant's foot, wet filament, heat creep, or a thermal runaway error. For designing or changing the part itself, use 3d-print instead.
---

# 3D Diagnose

Find the cause of an FDM print failure and give fixes the user can apply in their
slicer or on the printer. Diagnose from the first description — don't run an
intake form.

## Diagnosis flow

1. Read the description or photo (see "Reading a photo").
2. Diagnose immediately: ranked findings table plus fix steps (format below).
   Use `REFERENCE.md` for the symptom map, fix ranges, and material notes.
3. Ask one question only when it would change the top finding — and say which
   finding it settles. The most useful one is usually "what changed since prints
   last worked?" (new spool, nozzle, firmware, slicer profile, room temperature).
4. Ask about hardware (bed surface, extruder type, hotend, enclosure) only when the
   diagnosis depends on it.
5. After the fixes, ask the user to reprint and report back:
   - Same failure → check that the fix was applied, then move to hardware and
     calibration (belts, e-steps, PID, nozzle wear).
   - New failure → fresh diagnosis.
   - Resolved → close.

## Check the cheap causes first

Put these ahead of tuning when the symptoms fit, because each one mimics several
other failures and settings changes won't fix them:

- **Wet filament** — popping, stringing that wasn't there before, rough or weak
  prints, especially PETG, TPU, and nylon. Dry it and reprint before changing
  settings.
- **Dirty bed** — adhesion that got worse over time. Wash the plate.
- **Something changed** — a new spool or brand behaves like a different material.

**Thermal runaway errors are a safety fault, not a tuning problem.** Tell the user
to stop printing unattended, never to disable the protection, and follow item 16 in
REFERENCE.md.

## Reading a photo

Note where the defect is, because that narrows the cause:

- Only the first layers → bed, Z offset, first-layer settings, elephant's foot.
- At one height across the whole part → a layer shift or event at that height
  (collision, fan change, filament change).
- Repeating after corners or features → ringing.
- On overhangs, bridges, or one side only → cooling or geometry.
- Everywhere, getting worse over the print → extrusion: clog, heat creep, wet filament.

If the photo is too dark, blurry, or doesn't show the defect, ask for a close-up in
raking light along the surface.

## Multiple failures

- Triage by severity: print-stopping > functional (weak, wrong size) > cosmetic.
- Flag fixes that conflict: e.g. "Fix 1 raises temperature, which can worsen
  stringing from Fix 2 — apply Fix 2 first and check."

## Output format

```
| # | Failure | Confidence | Priority |
|---|---------|------------|----------|
| 1 | <name>  | High/Med/Low | Fix first/after/last |

## Fix 1: <Failure name>
- <Setting>: <current → target> (Cura: <name>, PrusaSlicer: <name>, OrcaSlicer/Bambu: <name>)
- <Hardware action if needed>

**Conflict note:** <if this fix conflicts with another>
**If this doesn't fix it:** <next step>
```

Use generic setting names with the slicer aliases from REFERENCE.md. When the user
has said which slicer they use, give only that slicer's name. Give one change at a
time where possible, so the reprint shows which fix worked.

## Failure list

REFERENCE.md has the symptoms and fix ranges for each. Name only the failures that
match; don't run through the list.

1. Wet filament
2. Stringing / oozing
3. Under-extrusion / weak layers
4. Over-extrusion / blobbing
5. Warping / bed adhesion failure
6. Layer separation / delamination
7. Layer shifting
8. Ringing / ghosting
9. First layer issues
10. Clogged nozzle / grinding filament
11. Elephant's foot
12. Bridging failure
13. Support issues
14. Dimensional inaccuracy
15. Heat creep
16. Thermal runaway (safety)

## When the cause is the model

Some failures are fixed in the design, not the slicer. Hand these to the
`3d-print` skill and name the parameter to change:

- Overhangs steeper than 45° or bridges over 20 mm → chamfers, teardrop holes,
  reorientation, or a support pillar in the model.
- Sharp-cornered large flat parts warping → round the corners in the model.
- Parts that split along layers under load → reorient so the load runs along layers.
- Elephant's foot stopping a part seating → bottom chamfer in the model.
- Holes too small while outer dimensions are right → hole compensation in the model.
- Walls thinner than two line widths (~0.9 mm) → thicker walls in the model.

Say: "Root cause is geometry. Use the `3d-print` skill to change: <parameter>."
Slicer-only fixes (wall count, brim, supports) stay here.
