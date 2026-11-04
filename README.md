# Skills

[![skills.sh](https://skills.sh/b/mjarlund/skills)](https://skills.sh/mjarlund/skills)

These are my personal agent skills that I create, use, and maintain across real projects.

I keep these skills small, composable, and tool-agnostic so they stay useful over time. This repo is intentionally broad: it includes any skill I actively maintain, not just one domain.

## Available skills

<!-- skills-start -->
- **[3d-print](skills/3d/3d-print/SKILL.md)** — Design 3D-printable parts via parametric CAD scripts, then export STL for slicing and printing. Use when user wants to create a part, enclosure, mount, bracket, adapter, or other printable model.
- **[3d-diagnose](skills/3d/3d-diagnose/SKILL.md)** — Diagnose FDM 3D print failures from text description or photo. Identifies root causes, prescribes slicer and hardware fixes, and iterates until resolved. Use when user describes a failed print, asks why their print looks wrong, or mentions stringing, warping, layer issues, shifting, or other print defects.
- **[xcode-parallel](skills/xcode/xcode-parallel/SKILL.md)** — Build, test, run and debug Xcode/Swift/iOS projects safely when several agents or git worktrees share one machine: per-worktree DerivedData and private simulators, queued same-worktree commands, throttled compiles. Use when running xcodebuild, simulator tests, simctl or Xcode MCP build/test tools. Self-test: [selftest.sh](skills/xcode/xcode-parallel/tests/selftest.sh).
<!-- skills-end -->

## Quickstart

Install with skills.sh:

```bash
npx skills@latest add mjarlund/skills
```

