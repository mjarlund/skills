---
name: 3d-print
description: Design 3D-printable parts via parametric CAD scripts, then export STL for slicing and printing. Use when user wants to create a part, enclosure, mount, bracket, adapter, or other printable model.
---

# 3D Print Skill

<what-to-do>

Drive the user to a manufacturable part definition, then produce a parametric CAD script and STL export path.

Start by asking this exact first question: "Should we use OpenSCAD or CadQuery for this part?"

Do not continue to geometry until the user selects one.

Interview the user across dimensions, material, tolerances, and assembly constraints before writing final geometry.

Ask one question at a time. For each question, include your recommended answer and why.

If a question can be answered by existing files in the repo, check files first and avoid asking the user.

Be tool agnostic. Do not force one CAD stack unless the user asks. Prefer whichever of these best fits the request:
- OpenSCAD when direct script-to-STL workflows are preferred.
- CadQuery when Python-driven parametrics or richer geometric composition helps.
- Equivalent parametric CAD script patterns in other tools when explicitly requested.

Preserve the same modeling intent across tools: parameters, constraints, clearances, and printability checks should match regardless of syntax.

Use this staged loop:
- Checkpoint A: Base body only. No fasteners, no clips, no decorative details.
- Checkpoint B: Functional features (holes, slots, channels, clips, cable paths, mating interfaces).
- Checkpoint C: Finish passes (fillets/chamfers/text/material tweaks) and final STL export guidance.

At each checkpoint:
- Write the updated script to a file in the workspace.
- Show the file path and a concise summary of what changed.
- Attempt a build/validation run for the selected tool to verify syntax.
- Report the exact command run and whether it passed or failed.
- If it fails, fix errors and re-run validation before asking for approval.
- Explain what changed and why.
- Run the printability checklist.
- Wait for approval before moving on.

When delivering a final answer, include:
- Final script file path.
- Parameter table with defaults.
- STL generation command or export step.
- Suggested slicer baseline settings.

</what-to-do>

<supporting-info>

## Core workflow

Pipeline:
1. Define intent and constraints.
2. Build parametric CAD script.
3. Write/update the CAD script file in the workspace.
4. Generate STL from the chosen CAD tool.
5. Slice in the user's slicer of choice.
6. Print, test fit, iterate.

Note: prefer editing the same script file through checkpoints instead of creating a new file each time.

Treat OpenSCAD as a first-class target, but keep instructions transferable across CAD tools.

## Requirements interview checklist

Clarify these before full geometry:
- Function: What does the part hold, protect, align, or attach to?
- Envelope: Maximum width, depth, height limits.
- Interfaces: Screws, inserts, rails, snap features, press fits, cable exits.
- Material: PLA, PETG, TPU, ABS, or other.
- Strength direction: Which axis sees load?
- Print constraints: Orientation preference, support tolerance, nozzle/layer assumptions.
- Fit class: Tight, nominal, or loose for each mating feature.

## Printability checklist

Run before each checkpoint:
- Bottom face flat for bed adhesion.
- Overhangs at or below 45 degrees when possible.
- Wall thickness at least 1.2 mm, default 2.0 mm.
- Bridge spans at or below 20 mm unless supports are accepted.
- Hole clearances adjusted by material:
    - PLA: +0.3 mm
    - PETG: +0.4 mm
    - TPU: +0.5 mm
- No zero-thickness geometry or self-intersections.

## Default design values

- Wall thickness: 2.0 mm
- Exterior fillet: 1.5 mm
- Bottom chamfer: 0.5 mm
- Layer height assumption: 0.2 mm (round critical Z heights accordingly)

## Parametric behavior

Expect natural-language revisions and map them to parameter edits:
- Make it 5 mm taller -> increase H by 5.
- Make walls thicker -> increase WALL.
- Looser fit -> increase clearance offset.
- Move mounting holes outwards -> update hole spacing parameters.

## Example patterns

OpenSCAD style starter:
```scad
W = 40;
D = 30;
H = 10;
WALL = 2;

difference() {
    cube([W, D, H], center = true);
    cube([W - 2*WALL, D - 2*WALL, H], center = true);
}
```

CadQuery style starter:
```python
import cadquery as cq

W, D, H = 40, 30, 10
WALL = 2.0

result = (
        cq.Workplane("XY")
        .box(W, D, H)
        .shell(-WALL)
)
```

## STL export expectations

Always include an explicit export step for the chosen tool.

Script file conventions:
- OpenSCAD: use `.scad` files (for example `models/part-name.scad`).
- CadQuery: use `.py` files (for example `models/part-name.py`).
- If the user does not provide a path, choose a sensible default path and state it explicitly.

CadQuery example:
```python
cq.exporters.export(
        result,
        "output.stl",
        exportType="STL",
        tolerance=0.01,
        angularTolerance=0.1,
)
```

OpenSCAD example:
```bash
openscad -o output.stl model.scad
```

## Checkpoint syntax/build validation

Validate at every checkpoint after writing the script file.

OpenSCAD validation command:
```bash
openscad -o /tmp/3d-print-check.stl <path-to-model.scad>
```

CadQuery validation command:
```bash
python <path-to-model.py>
```

If required tooling is not available, state that clearly and provide the exact command the user can run locally.

## Fastener and tolerance references

For standard dimensions, material offsets, and slicer defaults, refer to REFERENCE.md.

</supporting-info>
