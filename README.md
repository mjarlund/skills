# claude-skills

Personal Claude Code skills repo.

## Usage

Point Claude Code at this repo in your settings:

```json
{
  "skills": [
    "~/Documents/claude-skills"
  ]
}
```

Or symlink individual skills into `~/.claude/skills/`:

```bash
ln -s ~/Documents/claude-skills/3d-print ~/.claude/skills/3d-print
```

## Skills

| Skill | Description |
|-------|-------------|
| [3d-print](./3d-print/SKILL.md) | Generate 3D-printable parts as CadQuery/OpenSCAD scripts |

## Examples

- [Greenhouse corner rail brace](./3d-print/examples/greenhouse-corner-brace.scad) — 90° L-brace that snaps onto aluminium glazing bar junction, parametric PETG design
