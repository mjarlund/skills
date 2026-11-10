# Skills

[![skills.sh](https://skills.sh/b/mjarlund/skills)](https://skills.sh/mjarlund/skills)

These are my personal agent skills that I create, use, and maintain across real projects.

I keep these skills small, composable, and tool-agnostic so they stay useful over time. This repo is intentionally broad: it includes any skill I actively maintain, not just one domain.

## Available skills

<!-- skills-start -->
- **[3d-print](skills/3d/3d-print/SKILL.md)** — Design 3D-printable parts as parametric OpenSCAD or CadQuery scripts, verify the geometry at each checkpoint, and export STL. Use when the user wants to create or modify an enclosure, mount, bracket, adapter, or other printable part. Tools: [check_stl.py](skills/3d/3d-print/scripts/check_stl.py), [check_overlap.py](skills/3d/3d-print/scripts/check_overlap.py), [fit-coupon.scad](skills/3d/3d-print/assets/fit-coupon.scad).
- **[3d-diagnose](skills/3d/3d-diagnose/SKILL.md)** — Diagnose FDM print failures from a description or photo, rank causes, and prescribe slicer and hardware fixes with Cura, PrusaSlicer, and OrcaSlicer/Bambu setting names. Use when a print failed or looks wrong: stringing, warping, layer splits, shifts, ringing, clogs, wet filament, heat creep, thermal runaway.
- **[xcode-parallel](skills/xcode/xcode-parallel/SKILL.md)** — Build, test, run and debug Xcode/Swift/iOS projects safely when several agents or git worktrees share one machine: per-worktree DerivedData and private simulators, queued same-worktree commands, throttled compiles. Use when running xcodebuild, simulator tests, simctl or Xcode MCP build/test tools. Self-test: [selftest.sh](skills/xcode/xcode-parallel/tests/selftest.sh).
<!-- skills-end -->

## Quickstart

Install with skills.sh:

```bash
npx skills@latest add mjarlund/skills
```

